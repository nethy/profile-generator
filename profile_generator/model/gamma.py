import math
from functools import cache

from profile_generator.unit import Curve, Point
from profile_generator.util import search


def power_at(point: Point) -> Curve:
    g = math.log(point.y) / math.log(point.x)
    return lambda x: math.pow(x, g)


def algebraic_at(point: Point, exponent: float) -> Curve:
    if point.gradient < 1:
        return inverse_algebraic_at(point, exponent)
    g = math.pow(
        (math.pow(point.y / point.x, exponent) - 1) / (1 - math.pow(point.y, exponent)),
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


def inverse_algebraic_at(point: Point, exponent: float) -> Curve:
    g = math.pow(
        (math.pow(point.x / point.y, exponent) - 1) / (1 - math.pow(point.x, exponent)),
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


def log_at(point: Point) -> Curve:
    if math.isclose(point.x, point.y):
        return lambda x: x
    elif point.y < point.x:
        return inverse_log_at(point)
    g = log_coefficient(point)
    return log(g)


@cache
def log_coefficient(point: Point) -> float:
    if math.isclose(point.x, point.y):
        return 0
    return search.jump_search(1e-9, 1e3, lambda c: log(c)(point.x), point.y)


def log(coefficient: float) -> Curve:
    if math.isclose(coefficient, 0):
        return lambda x: x
    return lambda x: math.log(coefficient * x + 1) / math.log(coefficient + 1)


def log_derivative(coefficient: float) -> Curve:
    if math.isclose(coefficient, 0):
        return lambda _: 1
    return lambda x: coefficient / (coefficient * x + 1) / math.log(coefficient + 1)


@cache
def inverse_log_at(point: Point) -> Curve:
    g = search.jump_search(-1e3, -1e-12, lambda c: inverse_log(-c)(point.x), point.y)
    return inverse_log(-g)


def inverse_log(coefficient: float) -> Curve:
    return lambda x: (math.pow(coefficient + 1, x) - 1) / coefficient
