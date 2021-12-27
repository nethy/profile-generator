import math
from collections.abc import Callable

from profile_generator.model.color import constants
from profile_generator.unit import Curve, Line, Point

from . import gamma, sigmoid


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = damped_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow_curve = sigmoid.algebraic(3.5, gradient)
    highlight_curve = sigmoid.algebraic(1.75, gradient)
    return lambda x: shadow_curve(x) if x < 0.5 else highlight_curve(x)


def _split_gradient(gradient: float, ratio: float) -> tuple[float, float]:
    """
    (s+h)/2 = c
    s = 2c-h
    ---
    s-1 = r*(h-1)
    s-1 = rh-r
    s = rh-r+1
    ---
    2c-h = rh-r+1
    h(r+1) = 2c+r-1
    h = (2c+r-1)/(r+1)
    s = 2c-(2c+r-1)/(r+1) = (2cr+r-1)/(r+1)
    """
    highlight = (2 * gradient + ratio - 1) / (ratio + 1)
    shadow = 2 * gradient - highlight
    return (shadow, highlight)


def algebraic_gamma(exponent: float, x: float, y: float) -> Curve:
    g = math.pow(
        math.pow(y, exponent) / math.pow(x, exponent) / math.pow(1 - y, exponent)
        - 1 / math.pow(1 - x, exponent),
        1 / exponent,
    )
    roll_off = lambda x: math.pow(
        (math.pow(x, exponent) + math.pow(g * x, exponent))
        / (1 + math.pow(g * x, exponent)),
        1 / exponent,
    )
    return (
        lambda val: y / x * val
        if val < x
        else roll_off(val - x) * (1 - y) / roll_off(1 - x) + y
    )


def damped_gamma(x: float, y: float) -> Curve:
    highlight_line = Line.from_points(Point(x, y), Point(1, 1))
    g = (2 * y / x - (1 - y) / (1 - x)) / (1 - y) - 1 / (1 - x)
    roll_off = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else (
            roll_off(val - x) * (1 - y) / roll_off(1 - x)
            + y
            + highlight_line.get_y(val)
        )
        / 2
    )


_SHADOW_Y = constants.LUMINANCE_20_SRGB
_HIGHLIGHT_Y = constants.LUMINANCE_60_SRGB


def filmic(middle: Point, gradient: float) -> Curve:
    shadow_line = Line.from_points(Point(0, 0), middle)
    highlight_line = Line.from_points(middle, Point(1, 1))
    corected_gradient = (
        (shadow_line.gradient + highlight_line.gradient) / 2 * gradient
        + middle.gradient
        - (shadow_line.gradient + highlight_line.gradient) / 2
    )
    base_line = Line.at_point(corected_gradient, middle)
    shadow_x = base_line.get_x(_SHADOW_Y)
    shadow_y = _SHADOW_Y
    highlight_x = base_line.get_x(_HIGHLIGHT_Y)
    highlight_y = _HIGHLIGHT_Y
    shadow_curve = _shadow_curve(shadow_x, shadow_y, corected_gradient, 0.5)
    highlight_curve = _highlight_curve(highlight_x, highlight_y, corected_gradient)
    return (
        lambda val: shadow_curve(val)
        if val < shadow_x
        else base_line.get_y(val)
        if val < highlight_x
        else highlight_curve(val)
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
