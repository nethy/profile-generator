import math
from collections.abc import Callable
from functools import cache

from profile_generator.model import bezier, gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Line, Point
from profile_generator.util import search


def get_srgb_flat(grey18: float) -> Curve:
    return _as_srgb(grey18, get_linear_flat)


def get_lab_flat(grey18: float) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve = get_linear_flat(linear_grey18)
    return lambda x: lab.from_xyz_lum(curve(lab.to_xyz_lum(x * 100))) / 100


def get_linear_flat(linear_grey18: float) -> Curve:
    return _get_algebraic_flat(linear_grey18)


def _get_shadow_curve(midtone: Point, gradient: float) -> tuple[Curve, Curve]:
    """
    f(x) = a(x-b)^2+c

    f(0) = 0
    f(gx) = gy
    f'(gx) = m
    """
    if math.isclose(midtone.gradient, gradient):
        return (lambda x: midtone.gradient * x, lambda _: midtone.gradient)
    a = (gradient - midtone.y / midtone.x) / midtone.x
    b = midtone.x - 0.5 * gradient / a
    c = -a * b * b
    return (lambda x: a * (x - b) * (x - b) + c, lambda x: 2 * a * (x - b))


def _get_highlight_curve(midtone: Point, gradient: float) -> tuple[Curve, Curve]:
    """
    f(x) = a(x-b)^0.5+c

    f(1) = 1
    f(gx) = gy
    f'(gx) = m
    """
    if math.isclose((1 - midtone.y) / (1 - midtone.x), gradient):
        return (
            lambda x: (1 - midtone.y) / (1 - midtone.x) * x
            + 1
            - (1 - midtone.y) / (1 - midtone.x),
            lambda _: (1 - midtone.y) / (1 - midtone.x),
        )
    a, b, c = _get_highlight_coefficients(midtone, gradient)
    return (lambda x: a * math.sqrt(x - b) + c, lambda x: 0.5 * a / math.sqrt(x - b))


def _get_highlight_coefficients(
    midtone: Point, gradient: float
) -> tuple[float, float, float]:
    b = (math.pow(midtone.x - 0.5 * (midtone.y - 1) / gradient, 2) - midtone.x) / (
        midtone.x - (midtone.y - 1) / gradient - 1
    )
    a = 2 * gradient * math.sqrt(midtone.x - b)
    c = 1 - a * math.sqrt(1 - b)
    return (a, b, c)


@cache
def _get_algebraic_flat(linear_grey18: float) -> Curve:
    midtone = Point(linear_grey18, constants.GREY18_LINEAR)
    shadow = gamma.algebraic_at(midtone)
    highlight = gamma.algebraic_at(midtone, 0.25)
    mask = bezier.curve(
        [
            (Point(0, 0), 1),
            (Point(midtone.x * 0.5, 0), 1),
            (Point(midtone.x * 1.5, 1), 1),
            (Point(1, 1), 1),
        ]
    )

    def combined(x: float) -> float:
        return (1 - mask(x)) * shadow(x) + mask(x) * highlight(x)

    base_shadow = Line.from_points(Point(0, 0), midtone)
    base_mask = Line.from_points(Point(0, 0), Point(linear_grey18, 1))
    return (
        lambda x: (
            (1 - base_mask.get_y(x)) * base_shadow.get_y(x)
            + base_mask.get_y(x) * combined(x)
        )
        if x < linear_grey18
        else combined(x)
    )


def _as_srgb(grey18: float, curve_supplier: Callable[[float], Curve]) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve = curve_supplier(linear_grey18)
    return lambda x: srgb.gamma(curve(srgb.inverse_gamma(x)))


def get_srgb_contrast(grey18: float, gradient: float) -> Curve:
    contrast = get_linear_contrast(srgb.inverse_gamma(grey18), gradient)
    return lambda x: srgb.gamma(contrast(srgb.inverse_gamma(x)))


def get_lab_contrast(linear_grey18: float, gradient: float) -> Curve:
    contrast = get_linear_contrast(linear_grey18, gradient)
    return lambda x: lab.from_xyz_lum(contrast(lab.to_xyz_lum(x * 100))) / 100


_MASK = bezier.curve(
    [
        (p, 1)
        for p in (
            Point(0.5, 0),
            Point(0.5 + (1 - 0.5) * 0.25, 0),
            Point(0.5 + (1 - 0.5) * 0.75, 1),
            Point(1, 1),
        )
    ]
)


def get_linear_contrast(linear_grey18: float, gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    compression = _get_highlight_compression(linear_grey18)
    return _get_linear_compressed_contrast(gradient, compression)


def _get_linear_compressed_contrast(gradient: float, compression: float) -> Curve:
    shadow = sigmoid.exponential(gradient)
    highlight = sigmoid.exponential((gradient - 1) / compression + 1)

    def _curve(x: float) -> float:
        if x < 0.5:
            return shadow(x)
        else:
            ratio = _MASK(x)
            return (1 - ratio) * shadow(x) + ratio * highlight(x)

    shift_x = gamma.power_at(Point(constants.GREY18_LINEAR, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_LINEAR))
    return lambda x: shift_y(_curve(shift_x(x)))


_REFERENCE_GRADIENT = 1.5
_REFERENCE_X = srgb.inverse_gamma(0.95)

_MAX_COMPRESSION = 8


def _get_value_by_gradient(compression: float) -> float:
    contrast = _get_linear_compressed_contrast(_REFERENCE_GRADIENT, 1 / compression)
    return contrast(_REFERENCE_X)


_HL_COMP_TABLE = search.get_table(1 / _MAX_COMPRESSION, 1, 32, _get_value_by_gradient)


@cache
def _get_highlight_compression(linear_grey18: float) -> float:
    flat = get_linear_flat(linear_grey18)
    reference_contrast = _get_linear_compressed_contrast(_REFERENCE_GRADIENT, 1)
    target = reference_contrast(_REFERENCE_X) - 1 / 3 * (
        flat(_REFERENCE_X) - _REFERENCE_X
    )

    target_gradient = search.table_search(
        _HL_COMP_TABLE,
        _get_value_by_gradient,
        target,
    )

    return 1 / target_gradient
