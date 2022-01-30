import math

from profile_generator.unit import Curve
from profile_generator.util import validation


def algebraic(gradient: float, exponent: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    elif gradient < 1 and not math.isclose(exponent, 1):
        raise ValueError(
            f"Gradient must be greater than equal to 1. Actual value is {gradient}"
        )

    c = 2 * math.pow(math.pow(gradient, exponent) - 1, 1 / exponent)
    return _generic_algebraic(c, exponent, 0, 1)


def mask(begin: float, end: float) -> Curve:
    validation.is_in_closed_interval(begin, 0, 1)
    validation.is_in_closed_interval(end, 0, 1)
    if math.isclose(begin, end) or end < begin:
        return lambda x: x

    mask_curve = _generic_algebraic(8, 2, begin, end)

    def _curve(x: float) -> float:
        if x < begin:
            return 0
        elif x < end:
            return mask_curve(x)
        else:
            return 1

    return _curve


def _generic_algebraic(c: float, k: float, a: float, b: float) -> Curve:
    if math.isclose(c, 0):
        return lambda x: x
    o = (a + b) / 2
    offset = c * (a - o) / math.pow(1 + math.pow(c * abs(a - o), k), 1 / k)
    return lambda x: (
        (c * (x - o) / math.pow(1 + math.pow(c * abs(x - o), k), 1 / k) - offset)
        / (c * (b - o) / math.pow(1 + math.pow(c * abs(b - o), k), 1 / k) - offset)
    )
