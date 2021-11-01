import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Curve, Point

from . import bezier, gamma, sigmoid


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness, brightness_gradient = gamma.exp(*middle)

    contrast_correction = brightness_gradient(0) / middle.gradient

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient * contrast_correction)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


def contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadows = sigmoid.exp(gradient)
    highlights = sigmoid.linear(gradient)
    return lambda x: shadows(x) if x < 0.5 else highlights(x)


@cache
def bezier_gamma(x: float, y: float) -> Curve:
    points = [(Point(0, 0), 1), (Point(x, y), 3), (Point(1, 1), 1)]
    base = bezier.curve(points)
    corrector = gamma.linear(base(x), y) if x >= y else gamma.inverse_linear(base(x), y)
    return lambda val: corrector(base(val))
