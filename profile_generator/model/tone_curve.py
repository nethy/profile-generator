import math
from collections.abc import Callable

from profile_generator.model import bezier, gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


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


def _get_algebraic_flat(linear_grey18: float) -> Curve:
    midtone = Point(linear_grey18, constants.GREY18_LINEAR)
    exponent = math.sqrt(1 / midtone.gradient)
    return gamma.algebraic_at(midtone, exponent)


def _as_srgb(grey18: float, curve_supplier: Callable[[float], Curve]) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve = curve_supplier(linear_grey18)
    return lambda x: srgb.gamma(curve(srgb.inverse_gamma(x)))


def get_srgb_contrast(gradient: float) -> Curve:
    contrast = _get_linear_contrast(gradient)
    return lambda x: srgb.gamma(contrast(srgb.inverse_gamma(x)))


def get_lab_contrast(gradient: float) -> Curve:
    contrast = _get_linear_contrast(gradient)
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


def _get_linear_contrast(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.exponential(gradient)
    highlight = sigmoid.exponential(1 + (gradient - 1) / 2)

    def _curve(x: float) -> float:
        if x < 0.5:
            return shadow(x)
        else:
            ratio = _MASK(x)
            return (1 - ratio) * shadow(x) + ratio * highlight(x)

    shift_x = gamma.power_at(Point(constants.GREY18_LINEAR, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_LINEAR))
    return lambda x: shift_y(_curve(shift_x(x)))
