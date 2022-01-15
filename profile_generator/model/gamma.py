import math
from functools import cache

from profile_generator.unit import Curve, Point
from profile_generator.util import search


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
    y  = ((x^k+(ax)^k)/(1+(ax)^k))^(1/k)
    y' = ((x^k+(ax)^k)/(1+(ax)^k))^(1/k)/(x(ax)^k+x)
    """
    return lambda x: math.pow(
        (math.pow(x, exponent) + math.pow(coefficient * x, exponent))
        / (1 + math.pow(coefficient * x, exponent)),
        1 / exponent,
    )


def partial_algebraic_at(point: Point, gradient: float, exponent: float = 1.0) -> Curve:
    if math.isclose(gradient, 1) and math.isclose(point.gradient, 1):
        return lambda x: x
    g = math.pow(
        math.pow(gradient / (1 - point.y), exponent)
        - 1 / math.pow(1 - point.x, exponent),
        1 / exponent,
    )
    curve = algebraic(g, exponent)
    return lambda x: curve(x - point.x) / curve(1 - point.x) * (1 - point.y) + point.y


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


@cache
def log_at(middle: Point) -> Curve:
    g = search.jump_search(1e-12, 1e3, lambda x: log(x)(middle.x), middle.y)
    return log(g)


def log(coefficient: float) -> Curve:
    return lambda x: math.log(coefficient * x + 1) / math.log(coefficient + 1)
