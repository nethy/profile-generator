from collections.abc import Mapping
from typing import Any, Optional

from .object_schema import InvalidObjectError, InvalidTypeError
from .schema import Schema, SchemaError


class MapSchema(Schema):
    def __init__(self, value_schema: Schema):
        self._value_schema = value_schema

    def validate(self, data: Any) -> Optional[SchemaError]:
        if not isinstance(data, dict):
            return InvalidTypeError(dict)

        errors = self._get_errors(data)
        if len(errors.keys()) > 0:
            return InvalidObjectError(errors)
        else:
            return None

    def _get_errors(self, data: Any) -> Mapping[str, SchemaError]:
        return {
            member: error
            for member, value in data.items()
            if (error := self._value_schema.validate(value)) is not None
        }


def map_of(value_schema: Schema) -> Schema:
    return MapSchema(value_schema)
