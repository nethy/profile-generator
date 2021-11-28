import math
from collections.abc import Callable

from profile_generator.model import bezier
from profile_generator.unit import Curve, Line, Point

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
    shadow_gradient = (3 * gradient - 0.5) / 2.5
    highlight_gradient = (2 * gradient + 0.5) / 2.5
    exp = sigmoid.exp(shadow_gradient)
    sqrt = sigmoid.sqrt(highlight_gradient)
    lin = sigmoid.linear(highlight_gradient)
    weight = sigmoid.exp(4)
    return lambda x: (1 - weight(x)) * exp(x) + weight(x) * (sqrt(x) + lin(x)) / 2


def shadow_linear_gamma(x: float, y: float) -> Curve:
    g = y / x / (1 - y) - 1 / (1 - x)
    highlight = lambda x: (x + g * x) / (1 + g * x)
    return (
        lambda val: y / x * val
        if val < x
        else highlight(val - x) / (1 / (1 - y)) / highlight(1 - x) + y
    )


def interpolated_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    shift, _ = gamma.linear(x, 0.5)
    contrast = sigmoid.linear(2)
    weight = lambda val: contrast(shift(val))
    return lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)


def highlight_linear_gamma(x: float, y: float) -> Curve:
    shadow, _ = gamma.linear(x, y)
    return (
        lambda val: shadow((1 / x) * val) / (1 / y)
        if val < x
        else (1 - y) / (1 - x) * val + 1 - (1 - y) / (1 - x)
    )


def flat_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    shift, gradient = gamma.linear(x, 0.5)
    contrast = sigmoid.linear(4 / gradient(x))
    weight = lambda val: contrast(shift(val))
    return lambda val: (1 - weight(val)) * shadow.get_y(val) + weight(
        val
    ) * highlight.get_y(val)


def gradient_matching_linear(x: float, y: float) -> Curve:
    g = y / x - 1
    return lambda x: (x + g * x) / (1 + g * x)


def bezier_gamma(x: float, y: float) -> Curve:
    shadow = Line.from_points(Point(0, 0), Point(x, y))
    highlight = Line.from_points(Point(x, y), Point(1, 1))
    weight = bezier.curve(
        [
            (Point(0, 1), 1),
            (Point(x, 1), 1),
            (Point(x, x), 1),
            (Point(1, 0), 1),
        ]
    )
    return lambda val: weight(val) * shadow.get_y(val) + (
        1 - weight(val)
    ) * highlight.get_y(val)


def hybrid_gamma(x: float, y: float) -> Curve:
    base = interpolated_gamma(x, y)
    correction = shadow_linear_gamma(x, y)
    return lambda val: (base(val) + correction(val)) / 2
