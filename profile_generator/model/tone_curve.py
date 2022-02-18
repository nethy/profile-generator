import math

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


def get_srgb_flat(grey18: float) -> Curve:
    return _get_srgb_flat(grey18)[0]


def get_lab_flat(grey18: float) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve, _ = get_linear_flat(linear_grey18)
    return lambda x: lab.from_xyz_lum(curve(srgb.inverse_gamma(x))) / 100


def get_linear_flat(linear_grey18: float) -> tuple[Curve, Curve]:
    """
    gx, gy

    highlights:
    f(x) = a(x-b)^0.5+c

    f(1) = 1
    f(gx) = gy
    f'(gx) = gy/gx
    """
    midtone = Point(linear_grey18, constants.GREY18_LINEAR)
    b = (
        midtone.x
        * (
            midtone.x * math.pow(midtone.y - 1, 2) / (4 * math.pow(midtone.y, 2))
            - midtone.x * (midtone.y - 1) / midtone.y
            + midtone.x
            - 1
        )
        / (2 * midtone.x - midtone.x * (midtone.y - 1) / midtone.y - 1 - midtone.x)
    )
    a = (midtone.y - 1) / (math.sqrt(midtone.x - b) - math.sqrt(1 - b))
    c = 1 - a * math.sqrt(1 - b)
    return (
        lambda x: midtone.gradient * x if x < midtone.x else a * math.sqrt(x - b) + c,
        lambda x: midtone.gradient if x < midtone.x else a * 0.5 / math.sqrt(x - b),
    )


def _get_srgb_flat(grey18: float) -> tuple[Curve, Curve]:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve, derivative = get_linear_flat(linear_grey18)
    return (
        lambda x: srgb.gamma(curve(srgb.inverse_gamma(x))),
        lambda x: srgb.gamma_derivative(curve(srgb.inverse_gamma(x)))
        * derivative(srgb.inverse_gamma(x))
        * srgb.inverse_gamma_derivative(x),
    )


def compensate_gradient(grey18: float, gradient: float) -> float:
    _, derivative = _get_srgb_flat(grey18)
    return gradient / derivative(grey18) + 1 - 1 / derivative(grey18)


def get_srgb_contrast(gradient: float) -> Curve:
    return _get_contrast(gradient, constants.GREY18_SRGB, 2.5)


def get_lab_contrast(gradient: float) -> Curve:
    return _get_contrast(gradient, constants.GREY18_LAB, 3)


def _get_contrast(gradient: float, middle: float, shadow_exponent: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.algebraic(gradient, shadow_exponent)
    highlight = sigmoid.algebraic(gradient, 2)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(middle, 0.5))
    shift_y = gamma.power_at(Point(0.5, middle))
    return lambda x: shift_y(curve(shift_x(x)))
