import math
from collections.abc import Callable

from profile_generator.unit import Curve, Point

from . import gamma, sigmoid


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = shadow_linear_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow_curve = sigmoid.algebraic(3, gradient)
    highlight_curve = sigmoid.algebraic(1.5, gradient)
    return lambda x: shadow_curve(x) if x < 0.5 else highlight_curve(x)


def shadow_linear_gamma(x: float, y: float) -> Curve:
    g = y / x / (1 - y) - 1 / (1 - x)
    highlight = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) * (1 - y) / highlight(1 - x) + y
    )
