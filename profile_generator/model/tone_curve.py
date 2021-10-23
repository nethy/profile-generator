import math
from collections.abc import Callable

from profile_generator.unit import Point

from . import gamma, sigmoid
from .type import Curve


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = hybrid_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, contrast_curve_filmic)


_CONTRAST_WEIGHT = sigmoid.exp(2)


def contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 0):
        return lambda x: x
    shadows = sigmoid.exp((3 * gradient - 0.5) / 2.5)
    highlights = sigmoid.exp((2 * gradient + 0.5) / 2.5)
    return lambda x: (
        (1 - _CONTRAST_WEIGHT(x)) * shadows(x) + _CONTRAST_WEIGHT(x) * highlights(x)
    )


_GAMMA_WEIGHT = sigmoid.exp(1.414213562373095)


def hybrid_gamma(x: float, y: float) -> Curve:
    weight_gamma = gamma.exp(x, 0.5)
    weight = lambda val: _GAMMA_WEIGHT(weight_gamma(val))

    shadows = gamma.exp(x, y)
    highlights = gamma.log(x, y)
    return lambda val: (1 - weight(val)) * shadows(val) + weight(val) * highlights(val)


def hybrid_inverse_gamma(x: float, y: float) -> Curve:
    weight_gamma = gamma.inverse_exp(0.5, y)
    weight = lambda val: weight_gamma(_GAMMA_WEIGHT(val))

    shadows = gamma.inverse_exp(x, y)
    highlights = gamma.inverse_log(x, y)
    return lambda val: (1 - weight(val)) * shadows(val) + weight(val) * highlights(val)
