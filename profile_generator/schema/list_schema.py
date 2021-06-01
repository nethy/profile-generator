from collections.abc import Mapping
from dataclasses import dataclass
from functools import reduce
from typing import Any, Optional

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class ListSchema(Schema):
    def __init__(self, item_schema: Schema):
        self._item_schema = item_schema

    def validate(self, data: Any) -> Optional[SchemaError]:
        if not isinstance(data, list):
            return InvalidTypeError(list)

        errors = self._get_errors(data)
        if len(errors) > 0:
            return InvalidListError(errors)
        else:
            return None

    def _get_errors(self, data: Any) -> Mapping[int, SchemaError]:
        return {
            i + 1: error
            for i, item in enumerate(data)
            if (error := self._item_schema.validate(item)) is not None
        }

    def process(self, data: Any) -> Mapping[str, str]:
        if not isinstance(data, list):
            return super().process(data)

        combine = lambda acc, next: acc | self._item_schema.process(next)
        return reduce(combine, data, {})


@dataclass
class InvalidListError(SchemaError):
    errors: Mapping[int, SchemaError]


def list_of(item_schema: Schema) -> Schema:
    return ListSchema(item_schema)
