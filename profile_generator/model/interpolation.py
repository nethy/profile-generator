import math
from collections.abc import Callable

from profile_generator.unit import Curve
from profile_generator.util import validation


def interpolate(
    a: Curve,
    b: Curve,
    mean: Callable[[float, float, float], float],
    begin: float = 0.0,
    end: float = 1.0,
) -> Curve:
    validation.is_greater(end, begin)

    def _interpolate(x: float) -> float:
        if x < begin:
            return a(x)
        elif x > end:
            return b(x)
        else:
            return mean(a(x), b(x), 1 - (x - begin) / (end - begin))

    return _interpolate


def interpolate_values(
    a: float,
    b: float,
    mean: Callable[[float, float, float], float],
    x: float,
    begin: float = 0.0,
    end: float = 1.0,
) -> float:
    if x < begin:
        return a
    elif x > end:
        return b
    else:
        return mean(a, b, 1 - (x - begin) / (end - begin))


def linear(a: float, b: float, ratio: float) -> float:
    return ratio * a + (1 - ratio) * b


def geometric(a: float, b: float, ratio: float) -> float:
    return math.pow(a, ratio) * math.pow(b, 1 - ratio)


def hermite(a: float, b: float, ratio: float) -> float:
    weight = 3 * math.pow(ratio, 2) - 2 * math.pow(ratio, 3)
    return linear(a, b, weight)


def hermite_mask(
    begin: float, end: float, low: float = 0.0, high: float = 1.0
) -> Callable[[float], float]:
    validation.is_greater(end, begin)
    validation.is_greater(high, low)

    def base(x: float) -> float:
        return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1

    def mask(x: float) -> float:
        if x < begin:
            return low
        elif x > end:
            return high
        else:
            return (high - low) * base(1 - (x - begin) / (end - begin)) + low

    return mask
