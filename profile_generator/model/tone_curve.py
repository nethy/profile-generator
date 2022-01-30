from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.unit import Curve, Point

_MIDDLE_GREY = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    middle = Point(grey18, _MIDDLE_GREY)
    flat = gamma.log_at(middle)
    contrast = _contrast(gradient)
    return lambda x: contrast(flat(x))


def _contrast(gradient: float) -> Curve:
    shadow = sigmoid.algebraic(gradient, 3)
    highlight = sigmoid.algebraic(gradient, 2)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))
