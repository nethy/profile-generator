import math

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.unit import Curve, Point

_MIDDLE_GREY = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    midtone = Point(grey18, _MIDDLE_GREY)
    coefficient = gamma.log_coefficient(midtone)
    flat = gamma.log(coefficient)
    derivative = gamma.log_derivative(coefficient)
    corrected_gradient = gradient / derivative(grey18) + 1 - 1 / derivative(grey18)
    corrected_gradient = gradient
    contrast = _contrast(corrected_gradient, derivative)
    return lambda x: contrast(flat(x))


def _contrast(gradient: float, derivative: Curve) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.algebraic(gradient, 2 * math.sqrt(derivative(0)))
    highlight = sigmoid.algebraic(gradient, 2 * math.sqrt(derivative(1)))
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))
