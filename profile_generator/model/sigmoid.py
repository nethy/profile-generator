import math
from functools import cache

from profile_generator.unit import Curve
from profile_generator.util import search, validation


def algebraic(gradient: float, exponent: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    elif gradient < 1 and not math.isclose(exponent, 1):
        raise ValueError(
            f"Gradient must be greater than equal to 1. Actual value is {gradient}"
        )

    c = 2 * math.pow(math.pow(gradient, exponent) - 1, 1 / exponent)
    return _generic_algebraic(c, exponent, 0, 1)


def _generic_algebraic(c: float, k: float, a: float, b: float) -> Curve:
    if math.isclose(c, 0):
        return lambda x: x
    o = (a + b) / 2
    offset = c * (a - o) / math.pow(1 + math.pow(c * abs(a - o), k), 1 / k)
    return lambda x: (
        (c * (x - o) / math.pow(1 + math.pow(c * abs(x - o), k), 1 / k) - offset)
        / (c * (b - o) / math.pow(1 + math.pow(c * abs(b - o), k), 1 / k) - offset)
    )


def brightness_curve(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_gradient(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda _: 1
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


@cache
def brightness_at(x: float, y: float) -> Curve:
    validation.is_positive(x)
    validation.is_positive(y)
    validation.is_greater_or_equal(y, x)
    coeff = search.jump_search(0, 100, lambda b: brightness_curve(b)(x), y)
    return brightness_curve(coeff)


def contrast_curve(c: float) -> Curve:
    validation.is_greater_or_equal(c, 0)
    if math.isclose(c, 0):
        return lambda x: x
    return lambda x: (1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))) / (
        1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2))
    )


def contrast_gradient(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


_EXP_GRADIENT_SEARCH_TABLE = search.get_table(0, 20, 16, contrast_gradient)


@cache
def exponential(gradient: float) -> Curve:
    validation.is_greater_or_equal(gradient, 1)
    coeff = search.table_search(_EXP_GRADIENT_SEARCH_TABLE, contrast_gradient, gradient)
    return contrast_curve(coeff)
