from typing import TypeVar

T = TypeVar("T", int, float)


def is_in_closed_interval(value: T, low: float, high: float) -> T:
    rounded_value = _round(value)
    if rounded_value < low or rounded_value > high:
        raise ValueError(f"value must be in [{low}, {high}]: {value}")

    return value


def is_positive(value: T) -> T:
    v = _round(value)
    if v <= 0:
        raise ValueError(f"value must be positive: {value}")
    return value


def _round(value: T) -> T:
    return round(value, 9)
