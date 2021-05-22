import math
from collections.abc import Callable
from functools import cache

from profile_generator.unit import Line, Point, equals

_ITERATION_LIMIT = 100

_JUMPS = 5
_JUMP_PART = 2 ** _JUMPS

Curve = Callable[[float], float]


def brightness_curve(b: float) -> Curve:
    if equals(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_gradient(b: float) -> Curve:
    if equals(b, 0):
        return lambda x: 1
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


@cache
def brightness_midpoint(b: float) -> float:
    return _find(0, 1, brightness_curve(b), 0.5)


@cache
def _brightness_gradient_at_midpoint(b: float) -> float:
    midpoint = brightness_midpoint(b)
    return brightness_gradient(b)(midpoint)


def contrast_curve(c: float) -> Curve:
    if equals(c, 0):
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
    if equals(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


@cache
def find_contrast_gradient(gradient: float) -> float:
    return _find(-100, 100, contrast_gradient, gradient)


def curve(brightness: float, contrast: float) -> Curve:
    gradient = _brightness_gradient_at_midpoint(brightness)
    _contrast_curve = contrast_curve(contrast / gradient)
    _brightness_curve = brightness_curve(brightness)
    return lambda x: _contrast_curve(_brightness_curve(x))


def curve_with_hl_protection(brightness: float, contrast: float) -> Curve:
    _curve = curve(brightness, contrast)
    _damped_curve = curve(brightness, contrast / 2)
    midpoint = brightness_midpoint(brightness)

    def _merged_curve(x: float) -> float:
        if x < midpoint:
            return _curve(x)
        else:
            weight = (math.exp(-2 * x) - math.exp(-midpoint)) / (
                math.exp(-2) - math.exp(-midpoint)
            )
            return (1 - weight) * _curve(x) + weight * _damped_curve(x)

    return _merged_curve


@cache
def find_curve_brightness(grey: Point, c: float) -> float:
    fn = lambda b: curve(b, c)(grey.x)
    return _find(-100, 100, fn, grey.y)


def _find(lower_bound: float, upper_bound: float, fn: Curve, target: float) -> float:
    left, right = lower_bound, upper_bound
    mid = (left + right) / 2
    value = fn(mid)
    if equals(value, target):
        return mid

    if value < target:
        left, left_value, right, right_value = _jump_forward_until(
            mid, right, value, fn, target
        )
    else:
        left, left_value, right, right_value = _jump_backward_until(
            left, mid, value, fn, target
        )

    return _find_internal(left, left_value, right, right_value, fn, target)


def _jump_forward_until(
    left: float,
    right: float,
    origo_value: float,
    fn: Callable[[float], float],
    target: float,
) -> tuple[float, float, float, float]:
    jump = (right - left) / _JUMP_PART
    origo = left
    left, right = origo, origo + jump
    left_value, right_value = origo_value, fn(right)
    for _ in range(_JUMPS):
        if right_value > target or equals(right_value, target):
            break
        jump *= 2
        left, right = right, origo + jump
        left_value, right_value = origo_value, fn(right)
    return (left, left_value, right, right_value)


def _jump_backward_until(
    left: float,
    right: float,
    origo_value: float,
    fn: Callable[[float], float],
    target: float,
) -> tuple[float, float, float, float]:
    jump = (right - left) / _JUMP_PART
    origo = right
    left, right = origo - jump, origo
    left_value, right_value = fn(left), origo_value
    for _ in range(_JUMPS):
        if left_value < target or equals(left_value, target):
            break
        jump *= 2
        left, right = origo - jump, left
        left_value, right_value = fn(left), left_value
    return (left, left_value, right, right_value)


def _find_internal(
    lower_bound: float,
    lower_bound_value: float,
    upper_bound: float,
    upper_bound_value: float,
    fn: Curve,
    target: float,
) -> float:
    left, left_value, right, right_value = (
        lower_bound,
        lower_bound_value,
        upper_bound,
        upper_bound_value,
    )
    is_binary = True
    for _ in range(_ITERATION_LIMIT):
        if is_binary:
            guess = (left + right) / 2
        else:
            guess = left + (target - left_value) * (right - left) / (
                right_value - left_value
            )
        is_binary = not is_binary
        value = fn(guess)

        if equals(value, target):
            break

        if value < target:
            left = guess
            left_value = value
        else:
            right = guess
            right_value = value
    return guess
