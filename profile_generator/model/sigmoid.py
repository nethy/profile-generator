import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Line, Point
from profile_generator.util.search import _jump_search

Curve = Callable[[float], float]


def brightness_curve(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_gradient(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda _: 1
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


@cache
def brightness_midpoint(b: float) -> float:
    return _jump_search(0, 1, brightness_curve(b), 0.5)


@cache
def _brightness_gradient_at_midpoint(b: float) -> float:
    midpoint = brightness_midpoint(b)
    return brightness_gradient(b)(midpoint)


# y = (x+xb)/(1+bx)
# y' = ((1+b)(1+bx)-(x+bx)b) / (1+bx)^2 = (1+b+bx+b^2x-bx-b^2x) / (1+(bx)^2+2bx) = (1+b)/(1+bx)^2
# b = ?
# y/x = (1+b)/(1+xb)
# y/x + yxb/x = 1+b
# y/x + yb = 1+b
# y/x = 1 + b - yb
# y/x - 1 = (1-y)b
# b = (y-x)/x(1-y)

# y/(1+b) = x/(1+bx)
# (1+b)/y = 1/x + b
# (1+b)/y -b = 1/x
# (1+b-by)/y = 1/x
# x = y/(1+b-by)
# x' = ((1+b-by) - y(-b)) / (1+b-by)^2 = (1+b)/(1+b-by)^2
# b=?
# 1+b-by = y/x
# 1+(1-y)b = y/x
# b = (y-x)/(x(1-y)) = (y-x)/(x-xy)


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


@cache
def find_contrast_gradient(gradient: float) -> float:
    return _jump_search(-100, 100, contrast_gradient, gradient)


def _base_curve(brightness: float, contrast: float) -> Curve:
    gradient = _brightness_gradient_at_midpoint(brightness)
    _contrast_curve = contrast_curve(contrast / gradient)
    _brightness_curve = brightness_curve(brightness)
    return lambda x: _contrast_curve(_brightness_curve(x))


def curve(brightness: float, contrast: float, hl_protection: float = 1.0) -> Curve:
    _curve = _base_curve(brightness, contrast)
    if math.isclose(hl_protection, 1.0):
        return _curve

    _damped_curve = _base_curve(brightness, contrast / hl_protection)
    midpoint = brightness_midpoint(brightness)

    def _merged_curve(x: float) -> float:
        if x < midpoint:
            return _curve(x)
        else:
            weight = (2 ** (-x) - 2 ** (-midpoint)) / (0.5 - 2 ** (-midpoint))
            return (1 - weight) * _curve(x) + weight * _damped_curve(x)

    return _merged_curve


@cache
def find_curve_brightness(grey: Point, c: float) -> float:
    fn = lambda b: curve(b, c)(grey.x)
    return _jump_search(-100, 100, fn, grey.y)
