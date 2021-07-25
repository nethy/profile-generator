from __future__ import annotations

from profile_generator.util import validation

from .precision import DECIMALS, equals


class Strength:
    def __init__(self, value: float = 0):
        self._value = validation.is_in_closed_interval(value, -1, 1)

    @staticmethod
    def non_negative(value: float = 0) -> Strength:
        value = validation.is_in_closed_interval(value, 0, 1)
        return Strength(value)

    @property
    def value(self) -> float:
        return self._value

    def __repr__(self) -> str:
        return f"Strength(value={self.value:.{DECIMALS}f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Strength):
            return NotImplemented

        return equals(self.value, other.value)

    def __hash__(self) -> int:
        return hash(self._value)
