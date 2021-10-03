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

    inverse:
    y = (ln(c(x+0.5/c-0.5)/(1-c(x+0.5/c-0.5)))-ln(c(0+0.5/c-0.5)/(1-c(0+0.5/c-0.5)))) /
        (ln(c(1+0.5/c-0.5)/(1-c(1+0.5/c-0.5)))-ln(c(0+0.5/c-0.5)/(1-c(0+0.5/c-0.5))))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    elif gradient > 1:
        c = _contrast_of_gradient_exp(gradient)
        acc = math.exp(c * 0.5)
        offset = 1 / (1 + acc)
        scale = 1 / (1 + 1 / acc) - offset
        return lambda x: (1 / (1 + math.exp(c * (0.5 - x))) - offset) / scale
    else:
        c = _contrast_of_inverse_gradient_exp(gradient)
        offset_arg = (1 - c) / (1 + c)
        offset = math.log(offset_arg)
        scale = math.log(1 / offset_arg)
        return lambda x: (
            math.log((0.5 * (1 - c) + c * x) / (0.5 * (1 + c) - c * x)) - offset
        ) / (scale - offset)


def _gradient_of_contrast_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    acc = math.exp(c / 2)
    return (c * (acc + 1)) / (4 * (acc - 1))


def _contrast_of_gradient_exp(gradient: float) -> float:
    return jump_search(0, 100, _gradient_of_contrast_exp, gradient)


def _gradient_of_inverse_contrast_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    offset_arg = (1 - c) / (1 + c)
    offset = math.log(offset_arg)
    scale = math.log(1 / offset_arg)
    return 4 * c / (scale - offset)


def _contrast_of_inverse_gradient_exp(gradient: float) -> float:
    return -1 * jump_search(
        -0.999999999999, 0.000000000001, _gradient_of_inverse_contrast_exp, gradient
    )


def tone_curve_exp(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_exp)


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
    gamma_x_curve, gamma_x_gradient = gamma.exp(middle.x, 0.5)
    gamma_y_curve, gamma_y_gradient = gamma.inverse_exp(0.5, middle.y)
    gamma_gradient = gamma_x_gradient * gamma_y_gradient

    contrast_gradient = _get_contrast_gradient(middle, gradient, gamma_gradient)
    _curve = contrast_curve(contrast_gradient)

    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


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


def _get_contrast_gradient(
    grey: Point, gradient: float, gamma_gradient: float
) -> float:
    return (
        math.sqrt(grey.gradient) * gradient + grey.gradient - math.sqrt(grey.gradient)
    ) / gamma_gradient


_WEIGHT = contrast_curve_exp(4)


def contrast_curve_filmic(gradient: float) -> Curve:
    shadows = contrast_curve_exp(gradient)
    highlights = contrast_curve_abs(gradient)
    curve = lambda x: (1 - _WEIGHT(x)) * shadows(x) + _WEIGHT(x) * highlights(x)
    return deepen(curve, gradient)


def deepen(curve: Curve, gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadows = contrast_curve_exp(math.pow(gradient, 0.333333333))

    def _curve(x: float) -> float:
        if x < 0.5:
            return (1 - 2 * _WEIGHT(x)) * shadows(x) + 2 * _WEIGHT(x) * x
        else:
            return x

    return lambda x: _curve(curve(x))
