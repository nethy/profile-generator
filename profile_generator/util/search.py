import math
from collections.abc import Callable
from typing import MutableMapping

Function = Callable[[float], float]
LUT = MutableMapping[float, float]


def jump_search(
    lower_bound: float,
    upper_bound: float,
    fn: Function,
    target: float,
) -> float:
    left, right = lower_bound, upper_bound
    mid = (left + right) / 2
    value = fn(mid)
    if math.isclose(value, target):
        return mid

    if value < target:
        left, left_value, right, right_value = _jump_forward_until(
            mid, right, value, fn, target
        )
    else:
        left, left_value, right, right_value = _jump_backward_until(
            left, mid, value, fn, target
        )

    return _binary_search(left, left_value, right, right_value, fn, target)


_JUMPS = 5
_JUMP_PART = 2 ** _JUMPS


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
        if right_value > target or math.isclose(right_value, target):
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
        if left_value < target or math.isclose(left_value, target):
            break
        jump *= 2
        left, right = origo - jump, left
        left_value, right_value = fn(left), left_value
    return (left, left_value, right, right_value)


_ITERATION_LIMIT = 100


def _binary_search(
    lower_bound: float,
    lower_bound_value: float,
    upper_bound: float,
    upper_bound_value: float,
    fn: Function,
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

        if math.isclose(value, target):
            break

        if value < target:
            left = guess
            left_value = value
        else:
            right = guess
            right_value = value
    return guess
