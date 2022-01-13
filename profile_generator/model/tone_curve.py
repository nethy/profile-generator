from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.unit import Curve, Line, Point

_MIDDLE_GREY = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    middle = Point(grey18, _MIDDLE_GREY)
    flat = _flat(middle)
    contrast = _contrast(gradient)
    return lambda x: contrast(flat(x))


def _flat(middle: Point) -> Curve:
    highlight = gamma.power_at(middle)
    shadow = gamma.algebraic_at(middle, 1)
    return lambda x: (1 - shadow(x)) * shadow(x) + shadow(x) * highlight(x)


def _contrast(gradient: float) -> Curve:
    shadow = sigmoid.algebraic(gradient, 2.5)
    highlight = sigmoid.algebraic(gradient, 2)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))


def brightness(p: Point) -> Curve:
    base_line = Line(p.gradient, 0)
    threshold = base_line.get_x(_MIDDLE_GREY)
    highlight = gamma.partial_algebraic_at(
        Point(threshold, _MIDDLE_GREY), base_line.gradient
    )
    return lambda x: base_line.get_y(x) if x < threshold else highlight(x)
