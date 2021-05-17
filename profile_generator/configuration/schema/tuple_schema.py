from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Optional

from .list_schema import InvalidListError
from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class TupleSchema(Schema):
    def __init__(self, *item_schemas: Schema):
        self._item_schemas = item_schemas

    def validate(self, data: Any) -> Optional[SchemaError]:
        if not isinstance(data, list):
            return InvalidTypeError(tuple)
        elif len(data) != len(self._item_schemas):
            return InvalidListSizeError(len(self._item_schemas))

        errors = self._get_errors(data)
        if len(errors) > 0:
            return InvalidListError(errors)
        else:
            return None

    def _get_errors(self, data: Any) -> Mapping[int, SchemaError]:
        return {
            i + 1: error
            for i, (schema, item) in enumerate(zip(self._item_schemas, data))
            if (error := schema.validate(item)) is not None
        }


@dataclass
class InvalidListSizeError(SchemaError):
    expected_length: int


def tuple_of(*item_schemas: Schema) -> Schema:
    return TupleSchema(*item_schemas)
