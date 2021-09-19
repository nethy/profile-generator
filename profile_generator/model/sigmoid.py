import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Point
from profile_generator.util.search import jump_search

from . import gamma
from .gamma import Curve


@cache
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
def tone_curve_exp(middle: Point, gradient: float) -> Curve:
    gamma_x_curve, gamma_x_gradient = gamma.exp(middle.x, 0.5)
    if middle.y <= 0.5:
        gamma_y_curve, gamma_y_gradient = gamma.inverse_exp(0.5, middle.y)
    else:
        gamma_y_curve, gamma_y_gradient = gamma.exp(0.5, middle.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _get_contrast_gradient(middle, gradient, gamma_gradient)
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
def tone_curve_sqrt(middle: Point, gradient: float) -> Curve:
    """
    h(f(g(grey.x)))' = h'(f(g(grey.x))) * f(g(grey.x))' =
                       h'(f(g(grey.x))) * f'(g(grey.x)) * g'(grey.x)
    x = grey.x
    g(grey.x) = 0.5
    f(0.5) = 0.5
    h(0.5) = grey.y
    """
    return _tone_curve(middle, gradient, contrast_curve_sqrt)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    gamma_x_curve, gamma_x_gradient = gamma.piecewise(middle.x, 0.5)
    gamma_y_curve, gamma_y_gradient = gamma.piecewise(0.5, middle.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _get_contrast_gradient(middle, gradient, gamma_gradient)
    _curve = contrast_curve(contrast_gradient)

    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


@cache
def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


@cache
def tone_curve_hlp(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_hlp)


def tone_curve_abs(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_abs)


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


def contrast_curve_hlp(gradient: float) -> Curve:
    def _curve(x: float) -> float:
        curve_sqrt = contrast_curve_sqrt(gradient)
        curve_abs = contrast_curve_abs(gradient)
        if x < 0.5:
            return curve_sqrt(x)
        else:
            return curve_abs(x)

    return _curve


def contrast_curve_filmic(gradient: float) -> Curve:
    def _curve(x: float) -> float:
        curve_exp = contrast_curve_exp(gradient)
        curve_abs = contrast_curve_abs(gradient)
        if x < 0.5:
            return curve_exp(x)
        else:
            return (curve_exp(x) + curve_abs(x)) / 2.0

    return _curve


def _get_contrast_gradient(
    grey: Point, gradient: float, gamma_gradient: float
) -> float:
    return (
        math.sqrt(grey.gradient) * gradient + grey.gradient - math.sqrt(grey.gradient)
    ) / gamma_gradient
