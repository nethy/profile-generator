import math
from functools import cache

from profile_generator.util.search import jump_search

from .type import Curve


def linear(x: float, y: float) -> Curve:
    """
    y = (gx/(1+gx))/(g/(1+g))
    """
    g = (y - x) / (x * (1 - y))
    return _linear(g)


def power(x: float, y: float) -> Curve:
    """
    y = x^g
    """
    g = math.log(y) / math.log(x)
    curve = lambda val: math.pow(val, g)
    return curve


def _linear(g: float) -> Curve:
    return lambda x: (x + g * x) / (1 + g * x)


def _gradient_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(g * x + 1, 2)


def inverse_linear(x: float, y: float) -> Curve:
    g = (x - y) / (y * (1 - x))
    return _inverse_linear(g)


def _inverse_linear(g: float) -> Curve:
    return lambda x: x / (-g * x + g + 1)


def _gradient_inverse_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(1 - g * (x - 1), 2)


def sqrt(x: float, y: float) -> Curve:
    """
    y = x/sqrt(x^2+1), as bounded y = (x*sqrt(g+1))/sqrt(gx^2+1)
    """
    g = (math.pow(y / x, 2) - 1) / (1 - math.pow(y, 2))
    return _sqrt(g)


def _sqrt(g: float) -> Curve:
    return lambda x: (x * math.sqrt(g + 1)) / math.sqrt(g * math.pow(x, 2) + 1)


def _gradient_sqrt(g: float, x: float) -> float:
    return math.sqrt(g + 1) / math.pow(g * math.pow(x, 2) + 1, 3 / 2)


def inverse_sqrt(x: float, y: float) -> Curve:
    g = (math.pow(x / y, 2) - 1) / (1 - math.pow(x, 2))
    return _inverse_sqrt(g)


def _inverse_sqrt(g: float) -> Curve:
    return lambda x: x / math.sqrt(-g * math.pow(x, 2) + g + 1)


def _gradient_inverse_sqrt(g: float, x: float) -> float:
    return (g + 1) / math.pow(-g * math.pow(x, 2) + g + 1, 3 / 2)


@cache
def exp(x: float, y: float) -> Curve:
    g = jump_search(-100, 100, lambda g: _exp(g)(x), y)
    return _exp(g)


def _gradient_exp(g: float, x: float) -> float:
    """
    y' = 2a(exp(a)+1)exp(ax)/((exp(a)-1)(exp(ax)+1)^2)
    """
    if math.isclose(g, 0):
        return 1
    else:
        acc_g = math.exp(g)
        acc_gx = math.exp(g * x)
        return 2 * g * (acc_g + 1) * acc_gx / ((acc_g - 1) * math.pow(acc_gx + 1, 2))


def _exp(g: float) -> Curve:
    """
    y = (1/(1+exp(-ax))-0.5) / (1/(1+exp(-a))-0.5)
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: (1 / (1 + math.exp(-g * x)) - 0.5) / (
            1 / (1 + math.exp(-g)) - 0.5
        )


@cache
def inverse_exp(x: float, y: float) -> Curve:
    g = jump_search(-100, 100, lambda g: _inverse_exp(g)(x), y)
    return _inverse_exp(g)


def _gradient_inverse_exp(g: float, x: float) -> float:
    """
    y' = (2-2exp(2a))/(a(exp(a)(x-1)-x-1)(exp(a)(x+1)-x+1))
    """
    if math.isclose(g, 0):
        return 1
    else:
        return (2 - 2 * math.exp(2 * g)) / (
            g * (math.exp(g) * (x - 1) - x - 1) * (math.exp(g) * (x + 1) - x + 1)
        )


def _inverse_exp(g: float) -> Curve:
    """
    y = -ln(1/(x/(1+exp(-a))-x/2+0.5)-1)/a
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: -math.log(1 / (x / (1 + math.exp(-g)) - x / 2 + 0.5) - 1) / g


@cache
def log(x: float, y: float) -> Curve:
    g = jump_search(-0.999999999999, 100, lambda g: _log(g)(x), y)
    return _log(g)


def _log(g: float) -> Curve:
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: math.log(g * x + 1) / math.log(g + 1)


@cache
def inverse_log(x: float, y: float) -> Curve:
    g = jump_search(-100, 0.999999999999, lambda g: _inverse_log(g)(x), y)
    return _inverse_log(g)


def _inverse_log(g: float) -> Curve:
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: -(math.pow(1 - g, x) - 1) / g
