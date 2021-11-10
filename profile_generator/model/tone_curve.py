import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Curve, Line, Point

from . import gamma, sigmoid


@cache
def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = linear_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


@cache
def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    base = sigmoid.exp(gradient)
    protector = sigmoid.linear(gradient)
    return lambda x: base(x) if x < 0.5 else (base(x) + 2 * protector(x)) / 3


@cache
def linear_gamma(x: float, y: float) -> Curve:
    g = y / x / (1 - y) - 1 / (1 - x)
    highlight = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) / (1 / (1 - y)) / highlight(1 - x) + y
    )


def flat_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    weight = _get_weight_curve(x)
    return lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)


def hybrid_gamma(x: float, y: float) -> Curve:
    linear = linear_gamma(x, y)
    flat = flat_gamma(x, y)
    return lambda val: (linear(val) + flat(val)) / 2


_WEIGHT_CONTRAST = sigmoid.linear(4)


def _get_weight_curve(x: float) -> Curve:
    weight_shift = linear_gamma(x, 0.5)
    return lambda val: _WEIGHT_CONTRAST(weight_shift(val))
