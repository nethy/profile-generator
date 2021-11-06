import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Curve, Point

from . import bezier, gamma, sigmoid


def tone_curve_filmic(middle: Point, gradient: float) -> Curve:
    return _tone_curve(middle, gradient, _contrast_curve_filmic)


def _tone_curve(
    middle: Point, gradient: float, contrast_curve: Callable[[float], Curve]
) -> Curve:
    brightness, correction = bezier_gamma(*middle)

    shift_x = gamma.power(middle.y, 0.5)
    shift_y = gamma.power(0.5, middle.y)
    _contrast = contrast_curve(gradient * math.sqrt(correction))
    _shifted_contrast = lambda x: shift_y(_contrast(shift_x(x)))

    return lambda x: _shifted_contrast(brightness(x))


def _contrast_curve_filmic(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadows = sigmoid.exp(gradient)
    highlights = sigmoid.linear(gradient)
    return lambda x: shadows(x) if x < 0.5 else highlights(x)


@cache
def bezier_gamma(x: float, y: float) -> tuple[Curve]:
    points = [(Point(0, 0), 1), (Point(x, y), 1), (Point(1, 1), 1)]
    base = bezier.curve(points)
    corrector, gradient = (
        gamma.exp(base(x), y) if y >= x else gamma.inverse_exp(base(x), y)
    )
    return (lambda val: corrector(base(val)), gradient(0))
