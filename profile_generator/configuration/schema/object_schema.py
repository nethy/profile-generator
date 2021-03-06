from dataclasses import dataclass
from typing import Any, Dict, List

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class ObjectSchema(Schema):
    def __init__(self, **object_schema: Schema):
        self._object_schema = object_schema

    def validate(self, data: Any) -> List[SchemaError]:
        if not isinstance(data, dict):
            return [InvalidTypeError(dict)]

        return self._validate_object(data)

    def _validate_object(self, data: Any) -> List[SchemaError]:
        errors = self._collect_errors(data)

        if len(errors.keys()) > 0:
            return [InvalidObjectError(errors)]
        else:
            return []

    def _collect_errors(self, data: Any) -> Dict[str, SchemaError]:
        errors: Dict[str, SchemaError] = {}
        for name, value in data.items():
            error = self._get_member_error(name, value)
            if len(error) > 0:
                errors[name] = error[0]
        return errors

    def _get_member_error(self, name: str, value: Any) -> List[SchemaError]:
        if name not in self._object_schema.keys():
            return [UnkownMemberError()]
        else:
            member_schema = self._object_schema.get(name, _ANY_SCHEMA)
            return member_schema.validate(value)


class AnySchema(Schema):
    def validate(self, data: Any) -> List[SchemaError]:
        return []


_ANY_SCHEMA = AnySchema()


@dataclass
class InvalidObjectError(SchemaError):
    errors: Dict[str, SchemaError]


@dataclass
class UnkownMemberError(SchemaError):
    pass


def object_of(**object_schema: Schema) -> Schema:
    return ObjectSchema(**object_schema)
