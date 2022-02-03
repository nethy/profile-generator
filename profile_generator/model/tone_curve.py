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
    contrast = _contrast(corrected_gradient)
    return lambda x: contrast(flat(x))


def _contrast(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow_slope = 1 / math.pow(gradient, 3)
    highlight_slope = 1 / math.pow(gradient, 2)
    shadow_degree = _degree(gradient, shadow_slope)
    highlight_degree = _degree(gradient, highlight_slope)
    shadow = sigmoid.algebraic(gradient, shadow_degree)
    highlight = sigmoid.algebraic(gradient, highlight_degree)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))


def _degree(gradient: float, slope: float) -> float:
    return math.log((1 - slope) / slope + 1) / math.log(gradient)
