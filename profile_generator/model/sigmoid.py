import math
from functools import cache
from typing import Optional

from profile_generator.unit import Point
from profile_generator.unit.strength import Strength
from profile_generator.util.search import jump_search

from .gamma import (
    Curve,
    gamma_gradient_inverse_linear,
    gamma_gradient_inverse_sqrt,
    gamma_gradient_linear,
    gamma_gradient_sqrt,
    gamma_inverse_linear,
    gamma_inverse_sqrt,
    gamma_linear,
    gamma_of_inverse_linear,
    gamma_of_inverse_sqrt,
    gamma_of_linear,
    gamma_of_sqrt,
    gamma_sqrt,
)


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
    gamma_x = gamma_of_linear(grey.x, 0.5)
    gamma_x_curve = gamma_linear(gamma_x)
    gamma_x_gradient = gamma_gradient_linear(gamma_x)(grey.x)

    gamma_y = gamma_of_inverse_linear(0.5, grey.y)
    gamma_y_curve = gamma_inverse_linear(gamma_y)
    gamma_y_gradient = gamma_gradient_inverse_linear(gamma_y)(0.5)

    contrast_gradient = _correct_gradient(gradient, gamma_x_gradient * gamma_y_gradient)
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


def contrast_of_gradient_sqrt(gamma: float) -> float:
    """
    y'= sqrt(0.25c+1)/(sqrt(c(x-0.5)^2+1)*(c(x^2-x+0.25)+1)), x = 0.5
    """
    return 4 * (gamma ** 2 - 1)


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
    gamma_x = gamma_of_sqrt(grey.x, 0.5)
    gamma_x_curve = gamma_sqrt(gamma_x)
    gamma_x_gradient = gamma_gradient_sqrt(gamma_x)(grey.x)

    gamma_y = gamma_of_inverse_sqrt(0.5, grey.y)
    gamma_y_curve = gamma_inverse_sqrt(gamma_y)
    gamma_y_gradient = gamma_gradient_inverse_sqrt(gamma_y)(0.5)

    contrast_gradient = _correct_gradient(gradient, gamma_x_gradient * gamma_y_gradient)
    contrast = contrast_of_gradient_sqrt(contrast_gradient)
    _curve = contrast_curve_sqrt(contrast)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def contrast_of_gradient_abs(gradient: float) -> float:
    return 2 * (gradient - 1)


def contrast_curve_abs(c: float) -> Curve:
    """
    y = ((c(x-0.5)/(1+c|x-0.5|))/(c(-0.5)/(1+c|-0.5|)))/
        ((c(1-0.5)/(1+c|1-0.5|))/(c(-0.5)/(1+c|-0.5|)))
    """
    if math.isclose(c, 0):
        return lambda x: x
    else:
        return lambda x: (
            (c * (x - 0.5)) / (1 + c * abs(x - 0.5)) + (c / 2) / (1 + c / 2)
        ) / (c / (1 + c / 2))


@cache
def tone_curve_hybrid(
    grey: Point,
    gradient: float,
    hl_tone: Optional[Strength] = None,
    sh_tone: Optional[Strength] = None,
) -> Curve:
    gamma_x_curve, gamma_x_gradient = get_gamma_x(grey.x)
    gamma_y_curve, gamma_y_gradient = get_gamma_y(grey.y)

    contrast_gradient = _correct_gradient(gradient, gamma_x_gradient * gamma_y_gradient)

    _curve = contrast_curve_sqrt(contrast_of_gradient_sqrt(contrast_gradient))
    _curve_abs = contrast_curve_abs(contrast_of_gradient_abs(contrast_gradient))

    hl_weight = ((hl_tone or Strength(1)).value + 1) / 2
    sh_weight = ((sh_tone or Strength(1)).value + 1) / 2

    def _compsite_curve(x: float) -> float:
        if x <= grey.x:
            return math.pow(
                gamma_y_curve(_curve(gamma_x_curve(x))), sh_weight
            ) * math.pow(gamma_y_curve(_curve_abs(gamma_x_curve(x))), 1 - sh_weight)
        else:
            return math.pow(
                gamma_y_curve(_curve(gamma_x_curve(x))), hl_weight
            ) * math.pow(gamma_y_curve(_curve_abs(gamma_x_curve(x))), 1 - hl_weight)

    return _compsite_curve


def get_gamma_x(x: float) -> tuple[Curve, float]:
    gamma = gamma_of_sqrt(x, 0.5)
    curve = gamma_sqrt(gamma)
    gradient = gamma_gradient_sqrt(gamma)(x)
    return (curve, gradient)


def get_gamma_y(y: float) -> tuple[Curve, float]:
    gamma = gamma_of_inverse_sqrt(0.5, y)
    curve = gamma_inverse_sqrt(gamma)
    gradient = gamma_gradient_inverse_sqrt(gamma)(0.5)
    return (curve, gradient)


def _correct_gradient(gradient: float, gamma_gradient: float) -> float:
    return max(1.0, gradient / math.sqrt(gamma_gradient))
