import math
from collections.abc import Callable

from profile_generator.unit import PRECISION, Point

_ITERATION_LIMIT = 100


def brightness(b: float, x: float) -> float:
    if b == 0:
        return x
    else:
        return (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def contrast(c: float, x: float) -> float:
    if c == 0:
        return x
    elif c > 0:
        return (1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))) / (
            1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2))
        )
    else:
        n_c = 2 - 1 / (math.exp((-c - math.sqrt(-c + 2)) / 2))
        return (
            math.log((n_c * (x - 0.5) + 1) / (1 - n_c * (x - 0.5)))
            - math.log((-n_c / 2 + 1) / (1 + n_c / 2))
        ) / (
            math.log((n_c / 2 + 1) / (1 - n_c / 2))
            - math.log((-n_c / 2 + 1) / (1 + n_c / 2))
        )


def contrast_slope(c: float) -> float:
    return (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))


def curve(c: float, b: float, x: float) -> float:
    return contrast(c, brightness(b, x))


def curve_with_hl_protection(c: float, b: float, x: float) -> float:
    midpoint = _approximate_midpoint(b)
    if x < midpoint:
        return curve(c, b, x)
    else:
        return (1 - (x - midpoint) / (1 - midpoint)) * curve(c, b, x) + (
            x - midpoint
        ) / (1 - midpoint) * curve(c / 2, b, x)


def _approximate_midpoint(b: float) -> float:
    return _approximate(0, 1, lambda x: brightness(b, x), 0.5)


def approximate_brightness(grey: Point, c: float) -> float:
    return _approximate(-100, 100, lambda b: curve(c, b, grey.x), grey.y)


def _approximate(
    low: float, high: float, fn: Callable[[float], float], target: float
) -> float:
    guess = (low + high) / 2
    value = fn(guess)
    for _ in range(_ITERATION_LIMIT):
        if abs(target - value) < PRECISION:
            break

        if value < target:
            low = guess
        else:
            high = guess

        guess = (low + high) / 2
        value = fn(guess)
    return guess
