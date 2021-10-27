import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Point

from . import bezier, gamma, sigmoid
from .type import Curve


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = bezier_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


_CONTRAST_WEIGHT = sigmoid.exp(2)


def contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 0):
        return lambda x: x
    shadows = sigmoid.exp((3 * gradient - 0.5) / 2.5)
    highlights = sigmoid.exp((2 * gradient + 0.5) / 2.5)
    return lambda x: (
        (1 - _CONTRAST_WEIGHT(x)) * shadows(x) + _CONTRAST_WEIGHT(x) * highlights(x)
    )


@cache
def bezier_gamma(x: float, y: float) -> Curve:
    points = [(Point(0, 0), 1), (Point(x, y), 3), (Point(1, 1), 1)]
    base = bezier.curve(points)
    corrector = gamma.linear(base(x), y) if x >= y else gamma.inverse_linear(base(x), y)
    return lambda val: corrector(base(val))
