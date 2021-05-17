from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .list_schema import InvalidListError
from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class TupleSchema(Schema):
    def __init__(self, *item_schemas: Schema):
        self._item_schemas = item_schemas

    def validate(self, data: Any) -> Sequence[SchemaError]:
        if not isinstance(data, list):
            return [InvalidTypeError(tuple)]
        elif len(data) != len(self._item_schemas):
            return [InvalidListSizeError(len(self._item_schemas))]

        errors = self._get_errors(data)
        if len(errors.keys()) > 0:
            return [InvalidListError(errors)]
        else:
            return []

    def _get_errors(self, data: Any) -> Mapping[int, SchemaError]:
        return {
            i + 1: error
            for i, (schema, item) in enumerate(zip(self._item_schemas, data))
            for error in schema.validate(item)
        }


@dataclass
class InvalidListSizeError(SchemaError):
    expected_length: int


def tuple_of(*item_schemas: Schema) -> Schema:
    return TupleSchema(*item_schemas)
