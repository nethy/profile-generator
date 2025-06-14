import math

from profile_generator.model import gamma
from profile_generator.unit import Curve
from profile_generator.unit.point import Point
from profile_generator.util import validation


def hermite(begin: float, end: float, center: float = 0.5) -> Curve:
    """The function 2*x^3-3*x^2+1 transformed into the [begin, end] boundary,
    and the center adjusted to the given relative value.
    """
    validation.is_greater_or_equal(end, begin)
    validation.is_in_closed_interval(center, 0.1, 0.9)

    def base(x: float) -> float:
        return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1

    shift_center = gamma.algebraic_at(Point(center, 0.5))

    def fun(x: float) -> float:
        if x < begin:
            return 1
        elif x > end:
            return 0
        else:
            return base(shift_center((x - begin) / (end - begin)))

    return fun


def linear(begin: float, end: float) -> Curve:
    validation.is_greater_or_equal(end, begin)

    def fun(x: float) -> float:
        if x < begin:
            return 1
        elif x > end:
            return 0
        else:
            return 1 - (x - begin) / (end - begin)

    return fun
