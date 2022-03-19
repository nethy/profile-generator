import math
from typing import Callable

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


def get_srgb_flat(grey18: float) -> Curve:
    return _as_srgb(grey18, get_linear_flat)[0]


def get_lab_flat(grey18: float) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve, _ = get_linear_flat(linear_grey18)
    return lambda x: lab.from_xyz_lum(curve(srgb.inverse_gamma(x))) / 100


def get_linear_flat(linear_grey18: float) -> tuple[Curve, Curve]:
    """
    gx, gy

    shadows:
    f(x) = a(x-b)^2+c

    f(0) = 0
    f(gx) = gy
    f'(gx) = m

    highlights:
    f(x) = a(x-b)^0.5+c

    f(1) = 1
    f(gx) = gy
    f'(gx) = m
    """
    midtone = Point(linear_grey18, constants.GREY18_LINEAR)
    shadow, shadow_derivative = _get_shadow_curve(midtone, midtone.gradient)
    highlight, highlight_derivative = _get_highlight_curve(midtone, midtone.gradient)
    return (
        lambda x: shadow(x) if x < midtone.x else highlight(x),
        lambda x: shadow_derivative(x) if x < midtone.x else highlight_derivative(x),
    )


def _get_shadow_curve(midtone: Point, gradient: float) -> tuple[Curve, Curve]:
    if math.isclose(midtone.gradient, gradient):
        return (lambda x: midtone.gradient * x, lambda _: midtone.gradient)
    a = (gradient - midtone.y / midtone.x) / midtone.x
    b = midtone.x - 0.5 * gradient / a
    c = -a * b * b

    return (lambda x: a * (x - b) * (x - b) + c, lambda x: 2 * a * (x - b))


def _get_highlight_curve(midtone: Point, gradient: float) -> tuple[Curve, Curve]:
    b = (math.pow(midtone.x - 0.5 * (midtone.y - 1) / gradient, 2) - midtone.x) / (
        midtone.x - (midtone.y - 1) / gradient - 1
    )
    a = 2 * gradient * math.sqrt(midtone.x - b)
    c = 1 - a * math.sqrt(1 - b)

    return (lambda x: a * math.sqrt(x - b) + c, lambda x: 0.5 * a / math.sqrt(x - b))


def _as_srgb(
    grey18: float, curve_supplier: Callable[[float], tuple[Curve, Curve]]
) -> tuple[Curve, Curve]:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve, derivative = curve_supplier(linear_grey18)
    return (
        lambda x: srgb.gamma(curve(srgb.inverse_gamma(x))),
        lambda x: srgb.gamma_derivative(curve(srgb.inverse_gamma(x)))
        * derivative(srgb.inverse_gamma(x))
        * srgb.inverse_gamma_derivative(x),
    )


def get_srgb_contrast(gradient: float) -> Curve:
    contrast = _get_linear_contrast(gradient)
    return lambda x: srgb.gamma(contrast(srgb.inverse_gamma(x)))


def _get_linear_contrast(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.algebraic(gradient, 1.8)
    highlight = sigmoid.algebraic(gradient, 1.8)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(constants.GREY18_LINEAR, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_LINEAR))
    return lambda x: shift_y(curve(shift_x(x)))
