import math
from functools import cache

from profile_generator.util.search import jump_search

from .type import Curve


def linear(x: float, y: float) -> tuple[Curve, float]:
    """
    y = (gx/(1+gx))/(g/(1+g))
    """
    g = _coeff_of_linear(x, y)
    gradient = _gradient_linear(g, x)
    return (_linear(g), gradient)


def _linear(g: float) -> Curve:
    return lambda x: (x + g * x) / (1 + g * x)


def _gradient_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(g * x + 1, 2)


def _coeff_of_linear(x: float, y: float) -> float:
    return (y - x) / (x * (1 - y))


def inverse_linear(x: float, y: float) -> tuple[Curve, float]:
    g = _coeff_of_inverse_linear(x, y)
    gradient = _gradient_inverse_linear(g, x)
    return (_inverse_linear(g), gradient)


def _inverse_linear(g: float) -> Curve:
    return lambda x: x / (-g * x + g + 1)


def _gradient_inverse_linear(g: float, x: float) -> float:
    return (g + 1) / math.pow(1 - g * (x - 1), 2)


def _coeff_of_inverse_linear(x: float, y: float) -> float:
    return (x - y) / (y * (1 - x))


def sqrt(x: float, y: float) -> tuple[Curve, float]:
    """
    y = x/sqrt(x^2+1), as bounded y = (x*sqrt(g+1))/sqrt(gx^2+1)
    """
    g = _coeff_of_sqrt(x, y)
    gradient = _gradient_sqrt(g, x)
    return (_sqrt(g), gradient)


def _sqrt(g: float) -> Curve:
    return lambda x: (x * math.sqrt(g + 1)) / math.sqrt(g * math.pow(x, 2) + 1)


def _gradient_sqrt(g: float, x: float) -> float:
    return math.sqrt(g + 1) / math.pow(g * math.pow(x, 2) + 1, 3 / 2)


def _coeff_of_sqrt(x: float, y: float) -> float:
    return (math.pow(y / x, 2) - 1) / (1 - math.pow(y, 2))


def inverse_sqrt(x: float, y: float) -> tuple[Curve, float]:
    g = _coeff_of_inverse_sqrt(x, y)
    gradient = _gradient_inverse_sqrt(g, x)
    return (_inverse_sqrt(g), gradient)


def _inverse_sqrt(g: float) -> Curve:
    return lambda x: x / math.sqrt(-g * math.pow(x, 2) + g + 1)


def _gradient_inverse_sqrt(g: float, x: float) -> float:
    return (g + 1) / math.pow(-g * math.pow(x, 2) + g + 1, 3 / 2)


def _coeff_of_inverse_sqrt(x: float, y: float) -> float:
    return (math.pow(x / y, 2) - 1) / (1 - math.pow(x, 2))


def exp(x: float, y: float) -> tuple[Curve, float]:
    g = _coeff_of_exp(x, y)
    gradient = _gradient_exp(g, x)
    return (_exp(g), gradient)


def _gradient_exp(g: float, x: float) -> float:
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
def _coeff_of_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: _exp(g)(x), y)


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


def inverse_exp(x: float, y: float) -> tuple[Curve, float]:
    g = _coeff_of_inverse_exp(x, y)
    gradient = _gradient_inverse_exp(g, x)
    return (_inverse_exp(g), gradient)


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


@cache
def _coeff_of_inverse_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: _inverse_exp(g)(x), y)


def _inverse_exp(g: float) -> Curve:
    """
    y = -ln(1/(x/(1+exp(-a))-x/2+0.5)-1)/a
    """
    if math.isclose(g, 0):
        return lambda x: x
    else:
        return lambda x: -math.log(1 / (x / (1 + math.exp(-g)) - x / 2 + 0.5) - 1) / g


def piecewise(x: float, y: float) -> tuple[Curve, float]:
    """
    0  0
    gx gy
    1  1

    (1) f(gx) = gy
    (2) f(1) = 1
    (3) f'(gx) = gy/gx
    (4) f''(1) = 0

    f   = ax^3+bx^2+cx+d
    f'  = 3ax^2+2bx+c
    f'' = 6ax+2b
    """
    a = (1 - y / x) / 2 / (math.pow(x, 3) - 3 * math.pow(x, 2) + 3 * x - 1)
    b = -3 * a
    c = y / x - 3 * a * math.pow(x, 2) + 6 * a * x
    d = 2 * a * math.pow(x, 3) - 3 * a * math.pow(x, 2)

    def _curve(val: float) -> float:
        if val < x:
            return val * y / x
        else:
            weight = (val - x) / (1 - x)
            curve = a * math.pow(val, 3) + b * math.pow(val, 2) + c * val + d
            return (1 - weight) * curve + weight * val

    return (_curve, y / x)
