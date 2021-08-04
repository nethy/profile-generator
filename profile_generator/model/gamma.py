import math
from collections.abc import Callable
from functools import cache

from profile_generator.util.search import jump_search

Curve = Callable[[float], float]


def gamma_linear(g: float) -> Curve:
    """
    y = (gx/(1+gx))/(g/(1+g))
    """
    return lambda x: (x + g * x) / (1 + g * x)


def gamma_gradient_linear(g: float) -> Curve:
    return lambda x: (g + 1) / math.pow(g * x + 1, 2)


def gamma_of_linear(x: float, y: float) -> float:
    return (y - x) / (x * (1 - y))


def gamma_inverse_linear(g: float) -> Curve:
    return lambda x: x / (-g * x + g + 1)


def gamma_gradient_inverse_linear(g: float) -> Curve:
    return lambda x: (g + 1) / math.pow(1 - g * (x - 1), 2)


def gamma_of_inverse_linear(x: float, y: float) -> float:
    return (x - y) / (y * (1 - x))


def gamma_pow(g: float) -> Curve:
    """
    y = x^1/a
    """
    return lambda x: math.pow(x, 1 / g)


def gamma_gradient_pow(g: float) -> Curve:
    return lambda x: 1 / g * math.pow(x, 1 / g - 1)


def gamma_of_pow(x: float, y: float) -> float:
    return math.log(x) / math.log(y)


def gamma_inverse_pow(g: float) -> Curve:
    return lambda x: math.pow(x, g)


def gamma_gradient_inverse_pow(g: float) -> Curve:
    return lambda x: g * math.pow(x, g - 1)


def gamma_of_inverse_pow(x: float, y: float) -> float:
    return math.log(y) / math.log(x)


def gamma_sqrt(g: float) -> Curve:
    """
    y = x/sqrt(x^2+1), as bounded y = (x*sqrt(g+1))/sqrt(gx^2+1)
    """
    return lambda x: (x * math.sqrt(g + 1)) / math.sqrt(g * math.pow(x, 2) + 1)


def gamma_gradient_sqrt(g: float) -> Curve:
    return lambda x: math.sqrt(g + 1) / math.pow(g * math.pow(x, 2) + 1, 3 / 2)


def gamma_of_sqrt(x: float, y: float) -> float:
    return (math.pow(y / x, 2) - 1) / (1 - math.pow(y, 2))


def gamma_inverse_sqrt(g: float) -> Curve:
    return lambda x: x / math.sqrt(-g * math.pow(x, 2) + g + 1)


def gamma_gradient_inverse_sqrt(g: float) -> Curve:
    return lambda x: (g + 1) / math.pow(-g * math.pow(x, 2) + g + 1, 3 / 2)


def gamma_of_inverse_sqrt(x: float, y: float) -> float:
    return (math.pow(x / y, 2) - 1) / (1 - math.pow(x, 2))


def gamma_exp(g: float) -> Curve:
    """
    y = (e^(-ax)-1)/(e^(-a)-1)
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: (math.exp(-g * x) - 1) / (math.exp(-g) - 1)


def gamma_gradient_exp(g: float) -> Curve:
    """
    y' = -a*e^(-ax)/(e^(-a)-1)
    """
    if math.isclose(g, 0):
        return lambda _: 1
    else:
        return lambda x: (-g * math.exp(-g * x)) / (math.exp(-g) - 1)


@cache
def gamma_of_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: gamma_exp(g)(x), y)


def gamma_inverse_exp(g: float) -> Curve:
    """
    y = -ln(x(e^(-a)-1) + 1) / a
    invert a to allow binary search
    y = ln(x(e^a-1) + 1) / a
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: math.log(x * (math.exp(g) - 1) + 1) / g


def gamma_gradient_inverse_exp(g: float) -> Curve:
    """
    y' = (1-e^a)/(a(e^a*(x-1)-x))
    """
    if math.isclose(g, 0):
        return lambda _: 1
    else:
        return lambda x: (1 - math.exp(g)) / (g * (math.exp(g) * (x - 1) - x))


@cache
def gamma_of_inverse_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: gamma_inverse_exp(g)(x), y)
