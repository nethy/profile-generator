import math
from collections.abc import Callable

from profile_generator.unit import Curve, Point

from . import gamma, sigmoid


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness = algebraic_gamma(2/3, *middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient)
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow_deep = sigmoid.algebraic(2, 1.25 * gradient)
    shadow_base = sigmoid.algebraic(2, gradient)
    shadow_curve = lambda x: 2 * x * shadow_base(x) + (1 - 2 * x) * shadow_deep(x)
    highlight_curve = sigmoid.algebraic(1.5, gradient)
    return lambda x: shadow_curve(x) if x < 0.5 else highlight_curve(x)


def _split_gradient(gradient: float, ratio: float) -> tuple[float, float]:
    """
    (s+h)/2 = c
    s = 2c-h
    ---
    s-1 = r*(h-1)
    s-1 = rh-r
    s = rh-r+1
    ---
    2c-h = rh-r+1
    h(r+1) = 2c+r-1
    h = (2c+r-1)/(r+1)
    s = 2c-(2c+r-1)/(r+1) = (2cr+r-1)/(r+1)
    """
    highlight = (2 * gradient + ratio - 1) / (ratio + 1)
    shadow = 2 * gradient - highlight
    return (shadow, highlight)


def algebraic_gamma(grade: float, x: float, y: float) -> Curve:
    g = math.pow(
        math.pow(y, grade) / math.pow(x, grade) / math.pow(1 - y, grade)
        - 1 / math.pow(1 - x, grade),
        1 / grade,
    )
    highlight = lambda x: math.pow(
        (math.pow(x, grade) + math.pow(g * x, grade)) / (1 + math.pow(g * x, grade)),
        1 / grade,
    )
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) * (1 - y) / highlight(1 - x) + y
    )
