import math
from collections.abc import Callable

from profile_generator.unit import Point

from . import gamma, sigmoid
from .type import Curve


def tone_curve_sqrt(middle: Point, gradient: float) -> Curve:
    """
    h(f(g(grey.x)))' = h'(f(g(grey.x))) * f(g(grey.x))' =
                       h'(f(g(grey.x))) * f'(g(grey.x)) * g'(grey.x)
    x = grey.x
    g(grey.x) = 0.5
    f(0.5) = 0.5
    h(0.5) = grey.y
    """
    return _tone_curve(middle, gradient, sigmoid.sqrt)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    gamma_x_curve = gamma.exp(middle.x, 0.5)
    gamma_y_curve = gamma.inverse_exp(0.5, middle.y)

    _curve = contrast_curve(gradient)

    return lambda x: gamma_y_curve(_curve(gamma_x_curve(x)))


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


def tone_curve_abs(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, sigmoid.linear)


def tone_curve_exp(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, sigmoid.exp)


_WEIGHT = sigmoid.exp(2)


def contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 0):
        return lambda x: x
    shadows = sigmoid.exp(4 / 3 * gradient - 1 / 3)
    highlights = sigmoid.exp(2 / 3 * gradient + 1 / 3)
    return lambda x: (1 - _WEIGHT(x)) * shadows(x) + _WEIGHT(x) * highlights(x)


def hybrid_gamma(x: float, y: float) -> Curve:
    weight_gamma = gamma.exp(x, 0.5)
    weight = lambda val: _WEIGHT(weight_gamma(val))

    shadows = gamma.exp(x, y)
    highlights = gamma.linear(x, y)
    return lambda val: (1 - weight(val)) * shadows(val) + weight(val) * highlights(val)


def hybrid_inverse_gamma(x: float, y: float) -> Curve:
    weight_gamma = gamma.inverse_exp(0.5, y)
    weight = lambda val: weight_gamma(_WEIGHT(val))

    shadows = gamma.inverse_exp(x, y)
    highlights = gamma.inverse_linear(x, y)
    return lambda val: (1 - weight(val)) * shadows(val) + weight(val) * highlights(val)
