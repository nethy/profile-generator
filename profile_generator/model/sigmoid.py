import math
from functools import cache

from profile_generator.unit import Curve
from profile_generator.util.search import jump_search


@cache
def exp(gradient: float) -> Curve:
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
        c = _strength_of_gradient_exp(gradient)
        acc = math.exp(c * 0.5)
        offset = 1 / (1 + acc)
        scale = 1 / (1 + 1 / acc) - offset
        return lambda x: (1 / (1 + math.exp(c * (0.5 - x))) - offset) / scale
    else:
        c = _strength_of_inverse_gradient_exp(gradient)
        offset_arg = (1 - c) / (1 + c)
        offset = math.log(offset_arg)
        scale = math.log(1 / offset_arg)
        return lambda x: (
            math.log((0.5 * (1 - c) + c * x) / (0.5 * (1 + c) - c * x)) - offset
        ) / (scale - offset)


def _gradient_of_strength_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    acc = math.exp(c / 2)
    return (c * (acc + 1)) / (4 * (acc - 1))


def _strength_of_gradient_exp(gradient: float) -> float:
    return jump_search(0, 100, _gradient_of_strength_exp, gradient)


def _gradient_of_inverse_contrast_exp(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    offset_arg = (1 - c) / (1 + c)
    offset = math.log(offset_arg)
    scale = math.log(1 / offset_arg)
    return 4 * c / (scale - offset)


def _strength_of_inverse_gradient_exp(gradient: float) -> float:
    return -1 * jump_search(
        -0.999999999999, 0.000000000001, _gradient_of_inverse_contrast_exp, gradient
    )


def sqrt(gradient: float) -> Curve:
    """
    y = (c(x-0.5)/sqrt(1+c(x-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2)) /
        (c(1-0.5)/sqrt(1+c(1-0.5)^2)-c(-0.5)/sqrt(1+c(-0.5)^2))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _strength_of_gradient_sqrt(gradient)
        partial_result = c / math.sqrt(1 + c / 4)
        return (
            lambda x: (
                c * (x - 0.5) / math.sqrt(1 + c * math.pow(x - 0.5, 2))
                + partial_result / 2
            )
            / partial_result
        )


def _strength_of_gradient_sqrt(gradient: float) -> float:
    """
    y'= sqrt(0.25c+1)/(sqrt(c(x-0.5)^2+1)*(c(x^2-x+0.25)+1)), x = 0.5
    """
    return 4 * (math.pow(gradient, 2) - 1)


def linear(gradient: float) -> Curve:
    """
    y = ((c(x-0.5)/(1+c|x-0.5|))/(c(-0.5)/(1+c|-0.5|)))/
        ((c(1-0.5)/(1+c|1-0.5|))/(c(-0.5)/(1+c|-0.5|)))
    """
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _strength_of_gradient_abs(gradient)
        return lambda x: (
            (c * (x - 0.5)) / (1 + c * abs(x - 0.5)) + (c / 2) / (1 + c / 2)
        ) / (c / (1 + c / 2))


def _strength_of_gradient_abs(gradient: float) -> float:
    return 2 * (gradient - 1)


def algebraic(grade: float, gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    else:
        c = _strength_of_algebraic(grade, gradient)
        acc = c * 0.5 / math.pow(1 + c * math.pow(0.5, grade), 1 / grade)
        return lambda x: (
            (
                c
                * (x - 0.5)
                / math.pow(1 + c * math.pow(abs(x - 0.5), grade), 1 / grade)
                + acc
            )
            / (2 * acc)
        )


def _strength_of_algebraic(grade: float, gradient: float) -> float:
    return math.pow(2, grade) * (math.pow(gradient, grade) - 1)
