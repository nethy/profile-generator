import math
from collections.abc import Callable
from typing import MutableMapping

Function = Callable[[float], float]
LUT = MutableMapping[float, float]


def jump_search(
    lower_bound: float, upper_bound: float, fn: Function, target: float, lut: LUT
) -> float:
    left, right = lower_bound, upper_bound
    mid = (left + right) / 2
    value = _get_value(mid, fn, lut)
    if math.isclose(value, target):
        return mid

    if value < target:
        left, right = _jump_forward_until(mid, right, fn, target, lut)
    else:
        left, right = _jump_backward_until(left, mid, fn, target, lut)

    return binary_search(left, right, fn, target, lut)


_JUMPS = 5
_JUMP_PART = 2 ** _JUMPS


def _jump_forward_until(
    left: float, right: float, fn: Function, target: float, lut: LUT
) -> tuple[float, float]:
    jump = (right - left) / _JUMP_PART
    origo = left
    left, right = origo, origo + jump
    right_value = _get_value(right, fn, lut)
    for _ in range(_JUMPS):
        if right_value > target or math.isclose(right_value, target):
            break
        jump *= 2
        left, right = right, origo + jump
        right_value = _get_value(right, fn, lut)
    return (left, right)


def _jump_backward_until(
    left: float, right: float, fn: Function, target: float, lut: LUT
) -> tuple[float, float]:
    jump = (right - left) / _JUMP_PART
    origo = right
    left, right = origo - jump, origo
    left_value = _get_value(left, fn, lut)
    for _ in range(_JUMPS):
        if left_value < target or math.isclose(left_value, target):
            break
        jump *= 2
        left, right = origo - jump, left
        left_value = _get_value(left, fn, lut)
    return (left, right)


_ITERATION_LIMIT = 100


def binary_search(
    lower_bound: float,
    upper_bound: float,
    fn: Function,
    target: float,
    lut: LUT,
) -> float:
    left, right = lower_bound, upper_bound
    left_value, right_value = _get_value(left, fn, lut), _get_value(right, fn, lut)
    is_binary = True
    for _ in range(_ITERATION_LIMIT):
        if is_binary:
            guess = (left + right) / 2
        else:
            guess = left + (target - left_value) * (right - left) / (
                right_value - left_value
            )
        is_binary = not is_binary
        value = _get_value(guess, fn, lut)

        if math.isclose(value, target):
            break

        if value < target:
            left = guess
            left_value = value
        else:
            right = guess
            right_value = value
    return guess


def _get_value(x: float, fn: Function, lut: LUT) -> float:
    value = lut.get(x)
    if value is None:
        value = fn(x)
        lut[x] = value
    return value
