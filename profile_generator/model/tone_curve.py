import math
from collections.abc import Callable
from functools import cache

from profile_generator.model import bezier
from profile_generator.unit import Curve, Line, Point

from . import gamma, sigmoid


@cache
def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = hybrid_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


@cache
def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.exp(gradient)
    highlight = sigmoid.linear(gradient)
    return (
        lambda val: shadow(val) if val < 0.5 else (shadow(val) + 2 * highlight(val)) / 3
    )


@cache
def linear_gamma(x: float, y: float) -> Curve:
    g = y / x / (1 - y) - 1 / (1 - x)
    highlight = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) / (1 / (1 - y)) / highlight(1 - x) + y
    )


@cache
def flat_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    weight = bezier_weight(x)
    return lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)


@cache
def hybrid_gamma(x: float, y: float) -> Curve:
    linear = linear_gamma(x, y)
    flat = flat_gamma(x, y)
    return lambda val: (2*linear(val) + flat(val)) / 3


def bezier_weight(x: float) -> Curve:
    points = [(Point(0, 0), 1), (Point(x, 0), 1), (Point(x, 1), 1), (Point(1, 1), 1)]
    return bezier.curve(points)
