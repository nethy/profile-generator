from dataclasses import dataclass
from typing import Any, Dict, List

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class ListSchema(Schema):
    def __init__(self, item_schema: Schema):
        self._item_schema = item_schema

    def validate(self, data: Any) -> List[SchemaError]:
        if not isinstance(data, list):
            return [InvalidTypeError(list)]

        errors = self._get_errors(data)
        if len(errors) > 0:
            return [InvalidListError(errors)]
        else:
            return []

    def _get_errors(self, data: Any) -> Dict[int, SchemaError]:
        return {
            i + 1: error
            for i, item in enumerate(data)
            for error in self._item_schema.validate(item)
        }


@dataclass
class InvalidListError(SchemaError):
    errors: Dict[int, SchemaError]


def list_of(item_schema: Schema) -> Schema:
    return ListSchema(item_schema)
