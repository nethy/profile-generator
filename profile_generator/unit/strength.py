from __future__ import annotations

from profile_generator.util import validation


class Strength:
    def __init__(self, value: float = 0):
        self.__value = validation.is_in_closed_interval(value, 0, 1)

    @property
    def value(self) -> float:
        return self.__value

    def __repr__(self) -> str:
        return f"Strength(value={self.value:.3f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Strength):
            return NotImplemented

        return round(abs(self.value - other.value), 5) < 0.00001
