import math
from collections.abc import Callable

from profile_generator.unit import Curve, Line, Point

from . import gamma, sigmoid


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = flat_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.exp((3 * gradient - 0.5) / 2.5)
    higlight = sigmoid.exp((2 * gradient + 0.5) / 2.5)
    weight = sigmoid.exp(2)
    return lambda val: (1 - weight(val)) * shadow(val) + weight(val) * higlight(val)


def shadow_linear_gamma(x: float, y: float) -> Curve:
    g = y / x / (1 - y) - 1 / (1 - x)
    highlight = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) / (1 / (1 - y)) / highlight(1 - x) + y
    )


def interpolated_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    shift, _ = gamma.linear(x, 0.5)
    weight = lambda val: shift((val - x) / (1 - x))
    return (
        lambda val: shadow.get_y(val)
        if val < x
        else (1 - weight(val)) * shadow.get_y(val) + weight(val) * highlight.get_y(val)
    )


def highlight_linear_gamma(x: float, y: float) -> Curve:
    shadow, _ = gamma.linear(x, y)
    return (
        lambda val: shadow((1 / x) * val) / (1 / y)
        if val < x
        else (1 - y) / (1 - x) * val + 1 - (1 - y) / (1 - x)
    )


def flat_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    shift, _ = gamma.linear(x, 0.5)
    contrast = sigmoid.linear(4)
    weight = lambda val: contrast(shift(val))
    return lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)
