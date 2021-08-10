import math
from functools import cache

from profile_generator.unit import Point
from profile_generator.util.search import jump_search

from .gamma import (
    Curve,
    gamma_exp,
    gamma_inverse_exp,
    gamma_inverse_linear,
    gamma_inverse_sqrt,
    gamma_linear,
    gamma_sqrt,
)


def contrast_curve_exp(gradient: float) -> Curve:
    """
    y = (1/(1+exp(-c(x-0.5)))-1/(1+exp(-c(-0.5)))) /
        (1/(1+exp(-c(1-0.5)))-1/(1+exp(-c(-0.5))))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _contrast_of_gradient_exp(gradient)
        return lambda x: (
            1 / (1 + math.exp(c / 2 - c * x)) - 1 / (1 + math.exp(c / 2))
        ) / (1 / (1 + math.exp(-c / 2)) - 1 / (1 + math.exp(c / 2)))


def _gradient_of_contrast_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    return (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))


@cache
def _contrast_of_gradient_exp(gradient: float) -> float:
    return jump_search(0, 100, _gradient_of_contrast_exp, gradient)


@cache
def tone_curve_exp(grey: Point, gradient: float) -> Curve:
    gamma_x_curve, gamma_x_gradient = gamma_exp(grey.x, 0.5)
    if grey.y <= 0.5:
        gamma_y_curve, gamma_y_gradient = gamma_inverse_exp(0.5, grey.y)
    else:
        gamma_y_curve, gamma_y_gradient = gamma_exp(0.5, grey.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _correct_gradient(grey, gradient, gamma_gradient)
    _curve = contrast_curve_exp(contrast_gradient)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def contrast_curve_sqrt(gradient: float) -> Curve:
    """
    y = (c(x-0.5)/sqrt(1+c(x-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2)) /
        (c(1-0.5)/sqrt(1+c(1-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _contrast_of_gradient_sqrt(gradient)
        partial_result = c / math.sqrt(1 + c / 4)
        return (
            lambda x: (
                c * (x - 0.5) / math.sqrt(1 + c * math.pow(x - 0.5, 2))
                + partial_result / 2
            )
            / partial_result
        )


def _contrast_of_gradient_sqrt(gradient: float) -> float:
    """
    y'= sqrt(0.25c+1)/(sqrt(c(x-0.5)^2+1)*(c(x^2-x+0.25)+1)), x = 0.5
    """
    return 4 * (math.pow(gradient, 2) - 1)


@cache
def tone_curve_sqrt(grey: Point, gradient: float) -> Curve:
    """
    h(f(g(grey.x)))' = h'(f(g(grey.x))) * f(g(grey.x))' =
                       h'(f(g(grey.x))) * f'(g(grey.x)) * g'(grey.x)
    x = grey.x
    g(grey.x) = 0.5
    f(0.5) = 0.5
    h(0.5) = grey.y
    """
    gamma_x_curve, gamma_x_gradient = gamma_sqrt(grey.x, 0.5)
    gamma_y_curve, gamma_y_gradient = gamma_inverse_sqrt(0.5, grey.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _correct_gradient(grey, gradient, gamma_gradient)
    _curve = contrast_curve_sqrt(contrast_gradient)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def tone_curve_abs(grey: Point, gradient: float) -> Curve:
    gamma_x_curve, gamma_x_gradient = gamma_linear(grey.x, 0.5)
    gamma_y_curve, gamma_y_gradient = gamma_inverse_linear(0.5, grey.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _correct_gradient(grey, gradient, gamma_gradient)
    _curve = contrast_curve_abs(contrast_gradient)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def _contrast_of_gradient_abs(gradient: float) -> float:
    return 2 * (gradient - 1)


def contrast_curve_abs(gradient: float) -> Curve:
    """
    y = ((c(x-0.5)/(1+c|x-0.5|))/(c(-0.5)/(1+c|-0.5|)))/
        ((c(1-0.5)/(1+c|1-0.5|))/(c(-0.5)/(1+c|-0.5|)))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _contrast_of_gradient_abs(gradient)
        return lambda x: (
            (c * (x - 0.5)) / (1 + c * abs(x - 0.5)) + (c / 2) / (1 + c / 2)
        ) / (c / (1 + c / 2))


def _correct_gradient(grey: Point, gradient: float, gamma_gradient: float) -> float:
    return (
        math.sqrt(grey.gradient) * gradient + grey.gradient - math.sqrt(grey.gradient)
    ) / gamma_gradient
