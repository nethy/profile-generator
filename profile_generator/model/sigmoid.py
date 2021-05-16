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


def get_contrast(c: float) -> Curve:
    if equals(c, 0):
        return lambda x: x
    elif c > 0:
        return lambda x: (
            1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))
        ) / (1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2)))
    else:
        slope = 1 / contrast_slope(c)
        contrast_line = Line.at_point(slope, Point(0.5, 0.5))
        return contrast_line.get_y


def contrast_slope(c: float) -> float:
    if equals(c, 0):
        return 1
    return (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))


@cache
def find_contrast_slope(slope: float) -> float:
    return _find(-100, 100, contrast_slope, slope)


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
            weight = (math.exp(-2.1972179412841797 * x) - math.exp(-midpoint)) / (
                math.exp(-2.1972179412841797) - math.exp(-midpoint)
            )
            return (1 - weight) * curve(x) + weight * damped_curve(x)

    return _curve


@cache
def _find_brightness_midpoint(b: float) -> float:
    return _find(0, 1, get_brightness(b), 0.5)


@cache
def find_curve_brightness(grey: Point, c: float) -> float:
    return _find(-100, 100, lambda b: get_curve(c, b)(grey.x), grey.y)


def _find(
    low: float, high: float, fn: Callable[[float], float], target: float
) -> float:
    guess = (low + high) / 2
    value = fn(guess)
    for _ in range(_ITERATION_LIMIT):
        if equals(target, value):
            break

        if value < target:
            low = guess
        else:
            high = guess

        guess = (low + high) / 2
        value = fn(guess)
    return guess
