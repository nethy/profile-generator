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
    shadow_slope = 0.2 / derivative(0)
    highlight_slope = 0.2 / derivative(1)
    contrast = _contrast(gradient, shadow_slope, highlight_slope)
    return lambda x: contrast(flat(x))


def _contrast(gradient: float, shadow_slope: float, highlight_slope: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow_degree = math.log((1 - shadow_slope) / shadow_slope + 1) / math.log(gradient)
    highlight_degree = math.log((1 - highlight_slope) / highlight_slope + 1) / math.log(
        gradient
    )
    shadow = sigmoid.algebraic(gradient, shadow_degree)
    highlight = sigmoid.algebraic(gradient, highlight_degree)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.algebraic_at(Point(_MIDDLE_GREY, 0.5), 1)
    shift_y = gamma.algebraic_at(Point(0.5, _MIDDLE_GREY), 1)
    return lambda x: shift_y(curve(shift_x(x)))
