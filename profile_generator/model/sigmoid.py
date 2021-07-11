import math
from collections.abc import Callable

from profile_generator.unit import Line, Point
from profile_generator.util.search import _jump_search

Curve = Callable[[float], float]


def gamma_reciprocal(g: float) -> Curve:
    return lambda x: (x + g * x) / (1 + g * x)


def gamma_gradient_reciprocal(g: float) -> Curve:
    return lambda x: (1 + g) / (1 + g * x) ** 2


def gamma_of_reciprocal(x: float, y: float) -> float:
    return (y - x) / (x * (1 - y))


def gamma_inverse_reciprocal(g: float) -> Curve:
    return lambda x: x / (1 + g - g * x)


def gamma_inverse_gradient_reciprocal(g: float) -> Curve:
    return lambda x: (1 + g) / (1 + g - g * x) ** 2


def gamma_of_inverse_reciprocal(x: float, y: float) -> float:
    return (x - y) / (y - x * y)


def contrast_curve(c: float) -> Curve:
    if math.isclose(c, 0):
        return lambda x: x
    elif c > 0:
        return lambda x: (
            1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))
        ) / (1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2)))
    else:
        slope = 1 / contrast_gradient(c)
        contrast_line = Line.at_point(slope, Point(0.5, 0.5))
        return contrast_line.get_y


def contrast_gradient(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


def find_contrast_gradient(gradient: float) -> float:
    return _jump_search(-100, 100, contrast_gradient, gradient)


def tone_curve(grey: Point, gradient: float) -> Curve:
    contrast = find_contrast_gradient(gradient)

    gamma_x = gamma_of_reciprocal(grey.x, 0.5)
    gamma_x_curve = gamma_reciprocal(gamma_x)
    gamma_x_gradient = gamma_gradient_reciprocal(gamma_x)(grey.x)

    gamma_y = gamma_of_inverse_reciprocal(0.5, grey.y)
    gamma_y_curve = gamma_inverse_reciprocal(gamma_y)
    gamma_y_gradient = gamma_inverse_gradient_reciprocal(gamma_y)(0.5)

    _curve = contrast_curve(contrast / gamma_x_gradient / gamma_y_gradient)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def curve(middle: Point, gradient: float, hl_protection: float = 1.0) -> Curve:
    _curve = tone_curve(middle, gradient)
    if math.isclose(hl_protection, 1.0):
        return _curve

    _damped_curve = tone_curve(middle, gradient / hl_protection)

    def _merged_curve(x: float) -> float:
        if x < middle.x:
            return _curve(x)
        else:
            weight = (2 ** (-x) - 2 ** (-middle.x)) / (0.5 - 2 ** (-middle.x))
            return (1 - weight) * _curve(x) + weight * _damped_curve(x)

    return _merged_curve
