from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .schema import Schema, SchemaError


class TypeSchema(Schema):
    def __init__(self, data_type: type):
        self._data_type = data_type

    def validate(self, data: Any) -> Sequence[SchemaError]:
        if type(data) not in self._enhance(self._data_type):
            return [InvalidTypeError(self._data_type)]
        else:
            return []

    @staticmethod
    def _enhance(data_type: type) -> tuple[type, ...]:
        if data_type is float:
            return (data_type, int)
        else:
            return (data_type,)


@dataclass
class InvalidTypeError(SchemaError):
    expected_type: type


def type_of(data_type: type) -> Schema:
    return TypeSchema(data_type)
