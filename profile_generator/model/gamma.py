import math

from profile_generator.unit import Curve, Point


def power_at(ref: Point) -> Curve:
    g = math.log(ref.y) / math.log(ref.x)
    return lambda x: math.pow(x, g)


def algebraic_at(ref: Point, exponent: float) -> Curve:
    if ref.gradient < 1:
        return inverse_algebraic_at(ref, exponent)
    x, y = ref
    g = math.pow(
        (math.pow(y / x, exponent) - 1) / (1 - math.pow(y, exponent)), 1 / exponent
    )
    return algebraic(g, exponent)


def algebraic(coefficient: float, exponent: float) -> Curve:
    """
    y = ((x^k+(ax)^k)/(1+(ax)^k))^(1/k)
    """
    return lambda x: math.pow(
        (math.pow(x, exponent) + math.pow(coefficient * x, exponent))
        / (1 + math.pow(coefficient * x, exponent)),
        1 / exponent,
    )


def inverse_algebraic_at(ref: Point, exponent: float) -> Curve:
    x, y = ref
    g = math.pow(
        (math.pow(x / y, exponent) - 1) / (1 - math.pow(x, exponent)), 1 / exponent
    )
    return inverse_algebraic(g, exponent)


def inverse_algebraic(coefficient: float, exponent: float) -> Curve:
    """
    y = (x^k/(1+a^k(1-x^k)))^(1/k)
    """
    return lambda x: math.pow(
        math.pow(x, exponent)
        / (1 + math.pow(coefficient, exponent) * (1 - math.pow(x, exponent))),
        1 / exponent,
    )
