import math

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.unit import Curve, Line, Point

_SHADOW_Y = constants.LUMINANCE_25_SRGB
_HIGHLIGHT_Y = constants.LUMINANCE_50_SRGB
_MIDDLE_GREY = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    middle = Point(grey18, _MIDDLE_GREY)
    base = _base(middle)
    contrast = _contrast(gradient)
    return lambda x: contrast(base(x))


def _base(middle: Point) -> Curve:
    """
    0 0
    gx gy
    1 1

    f: [0, gx]

    f = a*x^2 + b*x + c
    f'= 2a*x + b

    f(0)   = 0
    f(gx)  = gy
    f'(gx) = 1
    """
    x, y = middle
    a = (x - y) / math.pow(x, 2)
    b = 2 * y / x - 1

    highlight = gamma.power_at(middle)

    return lambda x: a * math.pow(x, 2) + b * x if x < middle.x else highlight(x)


def _contrast(gradient: float) -> Curve:
    shadow = sigmoid.algebraic(gradient, 3)
    highlight = sigmoid.algebraic(gradient, 1.5)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))


def _filmic(gradient: float) -> Curve:
    middle = Point(_MIDDLE_GREY, _MIDDLE_GREY)
    shadow_line = Line.from_points(Point(0, 0), middle)
    highlight_line = Line.from_points(middle, Point(1, 1))
    corected_gradient = _corrected_gradient(
        middle, gradient, shadow_line, highlight_line
    )
    base_line = Line.at_point(middle, corected_gradient)
    shadow_latitude = (base_line.get_x(_SHADOW_Y), _SHADOW_Y)
    highlight_latitude = (base_line.get_x(_HIGHLIGHT_Y), _HIGHLIGHT_Y)
    shadow_curve = _shadow_curve(*shadow_latitude, corected_gradient, 1 / 2.2)
    highlight_curve = _highlight_curve(*highlight_latitude, corected_gradient, 1.8)
    return (
        lambda val: shadow_curve(val)
        if val < shadow_latitude[0]
        else base_line.get_y(val)
        if val < highlight_latitude[0]
        else highlight_curve(val)
    )


def brightness(ref: Point) -> Curve:
    base_line = Line(ref.gradient, 0)
    threshold = base_line.get_x(_MIDDLE_GREY)
    highlight = _highlight_curve(threshold, _MIDDLE_GREY, base_line.gradient, 1)
    return lambda x: base_line.get_y(x) if x < threshold else highlight(x)


def _corrected_gradient(
    middle: Point, gradient: float, shadow_line: Line, highlight_line: Line
) -> float:
    return (
        (shadow_line.gradient + highlight_line.gradient) / 2 * gradient
        + middle.gradient
        - (shadow_line.gradient + highlight_line.gradient) / 2
    )


def _shadow_curve(x: float, y: float, gradient: float, exponent: float = 1.0) -> Curve:
    if math.isclose(gradient, 1) and math.isclose(x, y):
        return lambda x: x
    g = _shadow_coefficient(x, y, gradient, exponent)
    curve = lambda x: math.pow(
        math.pow(x, exponent) / (math.pow(g, exponent) - math.pow(g * x, exponent) + 1),
        1 / exponent,
    )
    return lambda val: curve(val / x) * y


def _shadow_coefficient(x: float, y: float, gradient: float, exponent: float) -> float:
    return math.pow(gradient * x / y - 1, 1 / exponent)


def _highlight_curve(
    x: float, y: float, gradient: float, exponent: float = 1.0
) -> Curve:
    if math.isclose(gradient, 1) and math.isclose(x, y):
        return lambda x: x
    g = _highlight_coefficient(x, y, gradient, exponent)
    curve = lambda x: math.pow(
        (math.pow(x, exponent) + math.pow(g * x, exponent))
        / (math.pow(g * x, exponent) + 1),
        1 / exponent,
    )
    return lambda val: curve(val - x) / curve(1 - x) * (1 - y) + y


def _highlight_coefficient(
    x: float, y: float, gradient: float, exponent: float
) -> float:
    return math.pow(
        math.pow(gradient / (1 - y), exponent) - 1 / math.pow(1 - x, exponent),
        1 / exponent,
    )
