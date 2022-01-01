import math

from profile_generator.unit import Curve, Point


def power_at(point: Point) -> Curve:
    g = math.log(point.y) / math.log(point.x)
    return lambda x: math.pow(x, g)


def algebraic_at(p: Point, exponent: float) -> Curve:
    if p.gradient < 1:
        return inverse_algebraic_at(p, exponent)
    g = math.pow(
        (math.pow(p.y / p.x, exponent) - 1) / (1 - math.pow(p.y, exponent)),
        1 / exponent,
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


def partial_algebraic_at(p: Point, gradient: float, exponent: float = 1.0) -> Curve:
    if math.isclose(gradient, 1) and math.isclose(p.gradient, 1):
        return lambda x: x
    g = math.pow(
        math.pow(gradient / (1 - p.y), exponent) - 1 / math.pow(1 - p.x, exponent),
        1 / exponent,
    )
    curve = algebraic(g, exponent)
    return lambda x: curve(x - p.x) / curve(1 - p.x) * (1 - p.y) + p.y


def inverse_algebraic_at(p: Point, exponent: float) -> Curve:
    g = math.pow(
        (math.pow(p.x / p.y, exponent) - 1) / (1 - math.pow(p.x, exponent)),
        1 / exponent,
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


def partial_inverse_algebraic_at(
    p: Point, gradient: float, exponent: float = 1.0
) -> Curve:
    if math.isclose(gradient, 1) and math.isclose(p.gradient, 1):
        return lambda x: x
    g = math.pow(gradient * p.x / p.y - 1, 1 / exponent)
    curve = inverse_algebraic(g, exponent)
    return lambda x: curve(x / p.x) * p.y
