from dataclasses import dataclass
from typing import Any, List

from .schema import Schema, SchemaError


class RangeSchema(Schema):
    def __init__(self, left: int, right: int):
        self._left = left
        self._right = right

    def validate(self, data: Any) -> List[SchemaError]:
        if not (
            isinstance(data, int)
            and not isinstance(data, bool)
            and self._left <= data <= self._right
        ):
            return [InvalidRangeError(self._left, self._right)]
        else:
            return []


@dataclass
class InvalidRangeError(SchemaError):
    lower_bound: int
    upper_bound: int


def range_of(left: int, right: int) -> Schema:
    return RangeSchema(left, right)
