from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Try(Generic[T]):
    def __init__(self, value: T = None, error: Exception = None):
        if (value is None and error is None) or (
            value is not None and error is not None
        ):
            raise ValueError("only value or only error must be defined")
        self._value = value
        self._error = error

    @staticmethod
    def fail(error: Exception) -> Try[T]:
        return Try(error=error)

    @staticmethod
    def success(value: T) -> Try[T]:
        return Try(value=value)

    @property
    def value(self) -> T:
        if self._value is None:
            raise ValueError("No value")
        return self._value

    @property
    def error(self) -> Exception:
        if self._error is None:
            raise ValueError("No error")
        return self._error

    def succeeded(self) -> bool:
        return self._value is not None

    def __repr__(self) -> str:
        if self._value is not None:
            return f"Try(value={self._value!r})"
        else:
            return f"Try(error={self._error!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Try):
            return NotImplemented

        return self.value == other.value and self.error == other.error
