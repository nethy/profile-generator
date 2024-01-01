import bisect
import math
from collections.abc import Callable
from typing import Iterator, Mapping

Function = Callable[[float], float]


def get_table(
    lower_bound: float,
    upper_bound: float,
    table_size: int,
    fn: Function,
) -> Mapping[float, float]:
    if table_size < 2:
        raise ValueError(f"Table size cannot be less than 2: {table_size}")
    if lower_bound > upper_bound:
        raise ValueError(
            f"Lower bound {lower_bound} must not be greater "
            + "than upper bound: {upper_bound}"
        )

    return {
        key: fn(key) for key in _get_table_keys(lower_bound, upper_bound, table_size)
    }


def table_search(
    table: Mapping[float, float],
    fn: Function,
    target: float,
) -> float:
    keys, values = list(table.keys()), list(table.values())
    i = bisect.bisect_left(values, target)
    if math.isclose(values[i], target):
        return values[i]
    return _alternating_search(
        keys[i - 1],
        values[i - 1],
        keys[i],
        values[i],
        fn,
        target,
    )


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

    return _alternating_search(left, left_value, right, right_value, fn, target)


def _get_table_keys(
    lower_bound: float, upper_bound: float, table_size: int
) -> Iterator[float]:
    yield lower_bound
    for i in range(1, table_size - 1):
        yield (
            (1 - i / (table_size - 1)) * lower_bound
            + i / (table_size - 1) * upper_bound
        )
    yield upper_bound


_JUMPS = 5
_JUMP_PART = 2**_JUMPS


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
    fn: Function,
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


def _alternating_search(
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
    if target < lower_bound_value:
        return lower_bound
    if target > upper_bound_value:
        return upper_bound

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
