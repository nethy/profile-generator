import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Point
from profile_generator.util.search import jump_search

Curve = Callable[[float], float]


def gamma_sqrt(g: float) -> Curve:
    """
    y = x/sqrt(x^2+1), as bounded y = (x*sqrt(g+1))/sqrt(gx^2+1)
    """
    return lambda x: (x * math.sqrt(g + 1)) / math.sqrt(g * x ** 2 + 1)


def gamma_gradient_sqrt(g: float) -> Curve:
    return lambda x: math.sqrt(g + 1) / math.pow(g * x ** 2 + 1, 3 / 2)


def gamma_of_sqrt(x: float, y: float) -> float:
    return ((y / x) ** 2 - 1) / (1 - y ** 2)


def gamma_inverse_sqrt(g: float) -> Curve:
    return lambda x: x / math.sqrt(-g * x ** 2 + g + 1)


def gamma_gradient_inverse_sqrt(g: float) -> Curve:
    return lambda x: (g + 1) / math.pow(-g * x ** 2 + g + 1, 3 / 2)


def gamma_of_inverse_sqrt(x: float, y: float) -> float:
    return ((x / y) ** 2 - 1) / (1 - x ** 2)


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
        return lambda x: 1
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
        return lambda x: 1
    else:
        return lambda x: (1 - math.exp(g)) / (g * (math.exp(g) * (x - 1) - x))


@cache
def gamma_of_inverse_exp(x: float, y: float) -> float:
    return jump_search(-100, 100, lambda g: gamma_inverse_exp(g)(x), y)


def contrast_curve_exp(c: float) -> Curve:
    """
    y = (1/(1+exp(-c(x-0.5)))-1/(1+exp(-c(-0.5)))) /
        (1/(1+exp(-c(1-0.5)))-1/(1+exp(-c(-0.5))))
    """
    if math.isclose(c, 0):
        return lambda x: x
    else:
        return lambda x: (
            1 / (1 + math.exp(c / 2 - c * x)) - 1 / (1 + math.exp(c / 2))
        ) / (1 / (1 + math.exp(-c / 2)) - 1 / (1 + math.exp(c / 2)))


def gradient_of_contrast_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    return (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))


@cache
def contrast_of_gradient_exp(gradient: float) -> float:
    if math.isclose(gradient, 1):
        return 0
    else:
        return jump_search(0, 100, gradient_of_contrast_exp, gradient)


@cache
def tone_curve_exp(grey: Point, gradient: float) -> Curve:
    gamma_x = gamma_of_exp(grey.x, 0.5)
    gamma_x_curve = gamma_exp(gamma_x)
    gamma_x_gradient = gamma_gradient_exp(gamma_x)(grey.x)

    gamma_y = gamma_of_inverse_exp(0.5, grey.y)
    gamma_y_curve = gamma_inverse_exp(gamma_y)
    gamma_y_gradient = gamma_gradient_inverse_exp(gamma_y)(0.5)

    contrast_gradient = max(1.0, gradient / gamma_x_gradient / gamma_y_gradient)
    contrast = contrast_of_gradient_exp(contrast_gradient)
    _curve = contrast_curve_exp(contrast)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def contrast_curve_sqrt(c: float) -> Curve:
    """
    y = (c(x-0.5)/sqrt(1+c(x-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2)) /
        (c(1-0.5)/sqrt(1+c(1-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2))
    """
    if math.isclose(c, 0):
        return lambda x: x
    else:
        partial_result = c / math.sqrt(1 + c / 4)
        return (
            lambda x: (
                c * (x - 0.5) / math.sqrt(1 + c * (x - 0.5) ** 2) + partial_result / 2
            )
            / partial_result
        )


def contrast_of_gamma_sqrt(gamma: float) -> float:
    """
    y'= sqrt(0.25c+1)/(sqrt(c(x-0.5)^2+1)*(c(x^2-x+0.25)+1)), x = 0.5
    """
    return 4 * (gamma ** 2 - 1)


@cache
def tone_curve_sqrt(grey: Point, gamma: float) -> Curve:
    """
    h(f(g(grey.x)))' = h'(f(g(grey.x))) * f(g(grey.x))' =
                       h'(f(g(grey.x))) * f'(g(grey.x)) * g'(grey.x)
    x = grey.x
    g(grey.x) = 0.5
    f(0.5) = 0.5
    h(0.5) = grey.y
    """
    gamma_x = gamma_of_sqrt(grey.x, 0.5)
    gamma_x_curve = gamma_sqrt(gamma_x)
    gamma_x_gradient = gamma_gradient_sqrt(gamma_x)(grey.x)

    gamma_y = gamma_of_inverse_sqrt(0.5, grey.y)
    gamma_y_curve = gamma_inverse_sqrt(gamma_y)
    gamma_y_gradient = gamma_gradient_inverse_sqrt(gamma_y)(0.5)

    contrast_gradient = max(1.0, gamma / gamma_x_gradient / gamma_y_gradient)
    contrast = contrast_of_gamma_sqrt(contrast_gradient)
    _curve = contrast_curve_sqrt(contrast)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))
