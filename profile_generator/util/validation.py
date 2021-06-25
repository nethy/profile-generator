from typing import TypeVar

T = TypeVar("T", int, float)


def is_in_closed_interval(value: T, low: float, high: float) -> T:
    rounded_value = round(value, 9)
    if rounded_value < low or rounded_value > high:
        raise ValueError(f"value must be in [{low}, {high}], but it is {value}")

    return value
