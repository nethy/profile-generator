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
    brightness = flat_gamma(*middle)

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
    return lambda x: base(x) if x < 0.5 else (2 * base(x) + protector(x)) / 3


@cache
def flat_gamma(x: float, y: float) -> Curve:
    if math.isclose(x, y):
        return lambda val: val
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    weight_correction, _ = gamma.exp(x, 0.5)
    weight = lambda val: weight_curve(weight_correction(val))
    curve = lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)

    return (
        lambda val: curve(val)
        if val > x
        else (1 - val / x) * shadow.get_y(val) + val / x * curve(val)
    )


WEIGHT_EXP = sigmoid.exp(1.414213562373095)
WEIGHT_LINEAR = sigmoid.linear(1.414213562373095)


def weight_curve(x: float) -> float:
    return WEIGHT_EXP(WEIGHT_LINEAR(x))
