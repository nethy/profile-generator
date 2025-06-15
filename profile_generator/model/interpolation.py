import math
from collections.abc import Callable

from profile_generator.unit import Curve
from profile_generator.util import validation


def interpolate(
    a: Curve,
    b: Curve,
    average: Callable[[float, float, float], float],
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
            return average(a(x), b(x), 1 - (x - begin) / (end - begin))

    return _interpolate


def geometric(a: float, b: float, weight: float) -> float:
    return math.pow(a, weight) * math.pow(b, 1 - weight)
