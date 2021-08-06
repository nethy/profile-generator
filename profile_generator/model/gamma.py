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
    y = (1/(1+exp(-ax))-0.5) / (1/(1+exp(-a))-0.5)
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: (1 / (1 + math.exp(-g * x)) - 0.5) / (
            1 / (1 + math.exp(-g)) - 0.5
        )


def gamma_gradient_exp(g: float) -> Curve:
    """
    y' = 2a(exp(a)+1)exp(ax)/((exp(a)-1)(exp(ax)+1)^2)
    """
    if math.isclose(g, 0):
        return lambda _: 1
    else:
        return (
            lambda x: 2
            * g
            * (math.exp(g) + 1)
            * math.exp(g * x)
            / ((math.exp(g) - 1) * math.pow(math.exp(g * x) + 1, 2))
        )


@cache
def gamma_of_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: gamma_exp(g)(x), y)


def gamma_inverse_exp(g: float) -> Curve:
    """
    y = -ln(1/(x/(1+exp(-a))-x/2+0.5)-1)/a
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: -math.log(1 / (x / (1 + math.exp(-g)) - x / 2 + 0.5) - 1) / g


def gamma_gradient_inverse_exp(g: float) -> Curve:
    """
    y' = (2-2exp(2a))/(a(exp(a)(x-1)-x-1)(exp(a)(x+1)-x+1))
    """
    if math.isclose(g, 0):
        return lambda _: 1
    else:
        return lambda x: (2 - 2 * math.exp(2 * g)) / (
            g * (math.exp(g) * (x - 1) - x - 1) * (math.exp(g) * (x + 1) - x + 1)
        )


@cache
def gamma_of_inverse_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: gamma_inverse_exp(g)(x), y)
