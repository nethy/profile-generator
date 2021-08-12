import math
from collections.abc import Callable
from functools import cache

from profile_generator.util.search import jump_search

Curve = Callable[[float], float]


def gamma_linear(x: float, y: float) -> tuple[Curve, float]:
    """
    y = (gx/(1+gx))/(g/(1+g))
    """
    g = _gamma_of_linear(x, y)
    gradient = _gamma_gradient_linear(g, x)
    return (_gamma_linear(g), gradient)


def _gamma_linear(g: float) -> Curve:
    return lambda x: (x + g * x) / (1 + g * x)


def _gamma_gradient_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(g * x + 1, 2)


def _gamma_of_linear(x: float, y: float) -> float:
    return (y - x) / (x * (1 - y))


def gamma_inverse_linear(x: float, y: float) -> tuple[Curve, float]:
    g = _gamma_of_inverse_linear(x, y)
    gradient = _gamma_gradient_inverse_linear(g, x)
    return (_gamma_inverse_linear(g), gradient)


def _gamma_inverse_linear(g: float) -> Curve:
    return lambda x: x / (-g * x + g + 1)


def _gamma_gradient_inverse_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(1 - g * (x - 1), 2)


def _gamma_of_inverse_linear(x: float, y: float) -> float:
    return (x - y) / (y * (1 - x))


def gamma_sqrt(x: float, y: float) -> tuple[Curve, float]:
    """
    y = x/sqrt(x^2+1), as bounded y = (x*sqrt(g+1))/sqrt(gx^2+1)
    """
    g = _gamma_of_sqrt(x, y)
    gradient = _gamma_gradient_sqrt(g, x)
    return (_gamma_sqrt(g), gradient)


def _gamma_sqrt(g: float) -> Curve:
    return lambda x: (x * math.sqrt(g + 1)) / math.sqrt(g * math.pow(x, 2) + 1)


def _gamma_gradient_sqrt(g: float, x: float) -> float:
    return math.sqrt(g + 1) / math.pow(g * math.pow(x, 2) + 1, 3 / 2)


def _gamma_of_sqrt(x: float, y: float) -> float:
    return (math.pow(y / x, 2) - 1) / (1 - math.pow(y, 2))


def gamma_inverse_sqrt(x: float, y: float) -> tuple[Curve, float]:
    g = _gamma_of_inverse_sqrt(x, y)
    gradient = _gamma_gradient_inverse_sqrt(g, x)
    return (_gamma_inverse_sqrt(g), gradient)


def _gamma_inverse_sqrt(g: float) -> Curve:
    return lambda x: x / math.sqrt(-g * math.pow(x, 2) + g + 1)


def _gamma_gradient_inverse_sqrt(g: float, x: float) -> float:
    return (g + 1) / math.pow(-g * math.pow(x, 2) + g + 1, 3 / 2)


def _gamma_of_inverse_sqrt(x: float, y: float) -> float:
    return (math.pow(x / y, 2) - 1) / (1 - math.pow(x, 2))


def gamma_exp(x: float, y: float) -> tuple[Curve, float]:
    g = _gamma_of_exp(x, y)
    gradient = _gamma_gradient_exp(g, x)
    return (_gamma_exp(g), gradient)


def _gamma_gradient_exp(g: float, x: float) -> float:
    """
    y' = 2a(exp(a)+1)exp(ax)/((exp(a)-1)(exp(ax)+1)^2)
    """
    if math.isclose(g, 0):
        return 1
    else:
        return (
            2
            * g
            * (math.exp(g) + 1)
            * math.exp(g * x)
            / ((math.exp(g) - 1) * math.pow(math.exp(g * x) + 1, 2))
        )


@cache
def _gamma_of_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: _gamma_exp(g)(x), y)


def _gamma_exp(g: float) -> Curve:
    """
    y = (1/(1+exp(-ax))-0.5) / (1/(1+exp(-a))-0.5)
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: (1 / (1 + math.exp(-g * x)) - 0.5) / (
            1 / (1 + math.exp(-g)) - 0.5
        )


def gamma_inverse_exp(x: float, y: float) -> tuple[Curve, float]:
    g = _gamma_of_inverse_exp(x, y)
    gradient = _gamma_gradient_inverse_exp(g, x)
    return (_gamma_inverse_exp(g), gradient)


def _gamma_gradient_inverse_exp(g: float, x: float) -> float:
    """
    y' = (2-2exp(2a))/(a(exp(a)(x-1)-x-1)(exp(a)(x+1)-x+1))
    """
    if math.isclose(g, 0):
        return 1
    else:
        return (2 - 2 * math.exp(2 * g)) / (
            g * (math.exp(g) * (x - 1) - x - 1) * (math.exp(g) * (x + 1) - x + 1)
        )


@cache
def _gamma_of_inverse_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: _gamma_inverse_exp(g)(x), y)


def _gamma_inverse_exp(g: float) -> Curve:
    """
    y = -ln(1/(x/(1+exp(-a))-x/2+0.5)-1)/a
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: -math.log(1 / (x / (1 + math.exp(-g)) - x / 2 + 0.5) - 1) / g
