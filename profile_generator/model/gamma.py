import math
from functools import cache

from profile_generator.unit import Curve, Point
from profile_generator.util import search


def power_at(point: Point) -> Curve:
    g = power_exponent(point)
    return lambda x: math.pow(x, g)


def power_derivative_at(point: Point) -> Curve:
    g = power_exponent(point)
    return lambda x: g * math.pow(x, g - 1)


def power_exponent(point: Point) -> float:
    if math.isclose(point.x, 0):
        return 0
    elif math.isclose(point.x, 1):
        return math.inf
    return math.log(point.y) / math.log(point.x)


def algebraic_at(point: Point, exponent: float = 1.0) -> Curve:
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

    def curve(x: float) -> float:
        acc = math.pow(coefficient * x, exponent)
        return math.pow((math.pow(x, exponent) + acc) / (1 + acc), 1 / exponent)

    return curve


def exp2_at(point: Point) -> Curve:
    b = exp2_coefficient(point)
    print(b)
    return exp2(b)


@cache
def exp2_coefficient(point: Point) -> float:
    if math.isclose(point.x, point.y):
        return 0
    return search.jump_search(-1e3, 1e3, lambda c: exp2(c)(point.x), point.y)


def exp2(coefficient: float) -> Curve:
    """
    y  = (2^{-bx}-1)/(2^{-b}-1)
    y' = (2^{b(1-x)}*b*ld(2))/(2^b-1)
    """
    if math.isclose(coefficient, 0):
        return lambda x: x

    def curve(x: float) -> float:
        return (math.pow(2, -coefficient * x) - 1) / (math.pow(2, -coefficient) - 1)

    return curve


def partial_algebraic_at(point: Point, exponent: float = 1.0) -> Curve:
    if math.isclose(point.gradient, 1):
        return lambda x: x

    g = math.pow(
        math.pow(point.gradient / (1 - point.y), exponent)
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


def log_derivative_at(point: Point) -> Curve:
    if math.isclose(point.x, point.y):
        return lambda _: 1
    g = log_coefficient(point)
    return log_derivative(g)


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
