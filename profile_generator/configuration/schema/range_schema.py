from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from .schema import Schema, SchemaError
from .type_schema import type_of

T = TypeVar("T", int, float)


class RangeSchema(Generic[T], Schema):
    def __init__(self, left: T, right: T):
        self._left: T = left
        self._right: T = right
        self._type_schema = type_of(type(left))

    def validate(self, data: Any) -> Optional[SchemaError]:
        type_error = self._type_schema.validate(data)
        if not (type_error is None and self._left <= data <= self._right):
            return InvalidRangeError(self._left, self._right)
        else:
            return None


@dataclass
class InvalidRangeError(Generic[T], SchemaError):
    lower_bound: T
    upper_bound: T


def range_of(lower: T, upper: T) -> Schema:
    return RangeSchema(lower, upper)
