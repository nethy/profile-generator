import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Line, Point
from profile_generator.util.search import _jump_search

Curve = Callable[[float], float]


def brightness_curve(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_gradient(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: 1
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


@cache
def brightness_midpoint(b: float) -> float:
    return _jump_search(0, 1, brightness_curve(b), 0.5)


@cache
def _brightness_gradient_at_midpoint(b: float) -> float:
    midpoint = brightness_midpoint(b)
    return brightness_gradient(b)(midpoint)


def contrast_curve(c: float) -> Curve:
    if math.isclose(c, 0):
        return lambda x: x
    elif c > 0:
        return lambda x: (
            1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))
        ) / (1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2)))
    else:
        slope = 1 / contrast_gradient(c)
        contrast_line = Line.at_point(slope, Point(0.5, 0.5))
        return contrast_line.get_y


def contrast_gradient(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


@cache
def find_contrast_gradient(gradient: float) -> float:
    return _jump_search(-100, 100, contrast_gradient, gradient)


def _std_curve(brightness: float, contrast: float) -> Curve:
    gradient = _brightness_gradient_at_midpoint(brightness)
    _contrast_curve = contrast_curve(contrast / gradient)
    _brightness_curve = brightness_curve(brightness)
    return lambda x: _contrast_curve(_brightness_curve(x))


def curve(brightness: float, contrast: float, hl_protection: float = 1.0) -> Curve:
    _curve = _std_curve(brightness, contrast)
    if math.isclose(hl_protection, 1.0):
        return _curve

    _damped_curve = _std_curve(brightness, contrast / hl_protection)
    midpoint = brightness_midpoint(brightness)

    def _merged_curve(x: float) -> float:
        if x < midpoint:
            return _curve(x)
        else:
            weight = (2 ** (-x) - 2 ** (-midpoint)) / (0.5 - 2 ** (-midpoint))
            return (1 - weight) * _curve(x) + weight * _damped_curve(x)

    return _merged_curve


@cache
def find_curve_brightness(grey: Point, c: float) -> float:
    fn = lambda b: curve(b, c)(grey.x)
    return _jump_search(-100, 100, fn, grey.y)
