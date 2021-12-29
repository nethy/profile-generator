import math

from profile_generator.model.color import constants
from profile_generator.unit import Curve, Line, Point

_SHADOW_Y = constants.LUMINANCE_22_SRGB
_HIGHLIGHT_Y = constants.LUMINANCE_50_SRGB
_GREY_18_Y = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    middle = Point(grey18, _GREY_18_Y)
    shadow_line = Line.from_points(Point(0, 0), middle)
    highlight_line = Line.from_points(middle, Point(1, 1))
    corected_gradient = _corrected_gradient(
        middle, gradient, shadow_line, highlight_line
    )
    base_line = Line.at_point(middle, corected_gradient)
    shadow_latitude = (base_line.get_x(_SHADOW_Y), _SHADOW_Y)
    highlight_latitude = (base_line.get_x(_HIGHLIGHT_Y), _HIGHLIGHT_Y)
    shadow_curve = _shadow_curve(*shadow_latitude, corected_gradient, 0.5)
    highlight_curve = _highlight_curve(*highlight_latitude, corected_gradient)
    return (
        lambda val: shadow_curve(val)
        if val < shadow_latitude[0]
        else base_line.get_y(val)
        if val < highlight_latitude[0]
        else highlight_curve(val)
    )


def _corrected_gradient(
    middle: Point, gradient: float, shadow_line: Line, highlight_line: Line
) -> float:
    return (
        (shadow_line.gradient + highlight_line.gradient) / 2 * gradient
        + middle.gradient
        - (shadow_line.gradient + highlight_line.gradient) / 2
    )


def _shadow_curve(x: float, y: float, gradient: float, exponent: float = 1.0) -> Curve:
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
