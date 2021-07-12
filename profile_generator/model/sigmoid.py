import math
from collections.abc import Callable

from profile_generator.unit import Line, Point
from profile_generator.util.search import _jump_search

Curve = Callable[[float], float]


def gamma_reciprocal(g: float) -> Curve:
    """
    y = x/(1+x)
    """
    return lambda x: (x + g * x) / (1 + g * x)


def gamma_gradient_reciprocal(g: float) -> Curve:
    return lambda x: (1 + g) / (1 + g * x) ** 2


def gamma_of_reciprocal(x: float, y: float) -> float:
    return (y - x) / (x * (1 - y))


def gamma_inverse_reciprocal(g: float) -> Curve:
    return lambda x: x / (1 + g - g * x)


def gamma_inverse_gradient_reciprocal(g: float) -> Curve:
    return lambda x: (1 + g) / (1 + g - g * x) ** 2


def gamma_inverse_of_reciprocal(x: float, y: float) -> float:
    return (x - y) / (y - x * y)


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
    gamma_x = gamma_of_reciprocal(grey.x, 0.5)
    gamma_x_curve = gamma_reciprocal(gamma_x)
    gamma_x_gradient = gamma_gradient_reciprocal(gamma_x)(grey.x)

    gamma_y = gamma_inverse_of_reciprocal(0.5, grey.y)
    gamma_y_curve = gamma_inverse_reciprocal(gamma_y)
    gamma_y_gradient = gamma_inverse_gradient_reciprocal(gamma_y)(0.5)

    contrast = find_contrast_gradient(gradient / gamma_x_gradient / gamma_y_gradient)
    _curve = contrast_curve(contrast)
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


def contrast_of_gradient_sqrt(gradient: float) -> float:
    """
    y'= sqrt(0.25c+1)/(sqrt(c(x-0.5)^2+1)*(c(x^2-x+0.25)+1)), x = 0.5
    """
    return 4 * (gradient ** 2 - 1)


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

    contrast = contrast_of_gradient_sqrt(gradient / gamma_x_gradient / gamma_y_gradient)
    _curve = contrast_curve_sqrt(contrast)
    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def curve_sqrt(
    middle: Point,
    gradient: float,
    shadow_adjustment: float = 1.0,
    highlight_adjustment: float = 1.0,
) -> Curve:
    _curve = tone_curve_sqrt(middle, gradient)

    _shadow_curve = tone_curve_sqrt(middle, gradient * shadow_adjustment)
    _highlight_curve = tone_curve_sqrt(middle, gradient * highlight_adjustment)

    def _merged_curve(x: float) -> float:
        if x < middle.x:
            weight = x / middle.x
            return (1 - weight) * _shadow_curve(x) + weight * _curve(x)
        else:
            weight = (x - middle.x) / (1 - middle.x)
            return (1 - weight) * _curve(x) + weight * _highlight_curve(x)

    return _merged_curve
