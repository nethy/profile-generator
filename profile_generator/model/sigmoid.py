import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Line, Point, equals

_ITERATION_LIMIT = 100

Curve = Callable[[float], float]


def get_brightness(b: float) -> Curve:
    if equals(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_slope_at_midpoint(b: float) -> float:
    midpoint = _find_brightness_midpoint(b)
    return brightness_slope(b)(midpoint)


def brightness_slope(b: float) -> Curve:
    if equals(b, 0):
        return lambda x: x
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


def get_contrast(c: float) -> Curve:
    if equals(c, 0):
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
    if equals(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


@cache
def find_contrast_gradient(slope: float) -> float:
    return _find(-100, 100, contrast_gradient, slope)


def get_curve(c: float, b: float) -> Curve:
    brightness = get_brightness(b)
    contrast = get_contrast(c)
    return lambda x: contrast(brightness(x))


def get_curve_with_hl_protection(c: float, b: float) -> Curve:
    midpoint = _find_brightness_midpoint(b)
    curve = get_curve(c, b)
    damped_curve = get_curve(c / 2, b)

    def _curve(x: float) -> float:
        if x < midpoint:
            return curve(x)
        else:
            weight = (math.exp(-2 * x) - math.exp(-midpoint)) / (
                math.exp(-2) - math.exp(-midpoint)
            )
            return (1 - weight) * curve(x) + weight * damped_curve(x)

    return _curve


@cache
def _find_brightness_midpoint(b: float) -> float:
    return _find(0, 1, get_brightness(b), 0.5)


@cache
def find_curve_brightness(grey: Point, c: float) -> float:
    fn = lambda b: get_curve(c / brightness_slope_at_midpoint(b), b)(grey.x)
    return _find(-100, 100, fn, grey.y)


def _find(lower_bound: float, upper_bound: float, fn: Curve, target: float) -> float:
    left = lower_bound
    right = upper_bound
    for _ in range(_ITERATION_LIMIT):
        guess = (left + right) / 2
        value = fn(guess)

        if equals(value, target):
            break
        elif value < target:
            left = guess
        else:
            right = guess
    return guess
