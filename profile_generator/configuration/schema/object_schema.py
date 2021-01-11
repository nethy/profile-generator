from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

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
        errors: Dict[str, SchemaError] = {}
        for key, value in data.items():
            self._collect_errors(key, value, errors)

        if len(errors.keys()) > 0:
            return [InvalidObjectError(errors)]
        else:
            return []

    def _collect_errors(
        self, key: str, value: Any, errors: Dict[str, SchemaError]
    ) -> None:
        schema_members = self._object_schema.keys()
        nested_name, nested_value = self._get_nested_key_value(key, value)
        if nested_name not in schema_members:
            errors[nested_name] = UnkownMemberError()
        else:
            member_error = self._get_member_error(nested_name, nested_value)
            if len(member_error) > 0:
                errors[nested_name] = member_error[0]

    @staticmethod
    def _get_nested_key_value(key: str, value: Any) -> Tuple[str, Any]:
        dot_idx = key.find(".")
        if dot_idx > -1:
            return (key[:dot_idx], {key[dot_idx + 1 :]: value})
        else:
            return (key, value)

    def _get_member_error(self, name: str, value: Any) -> List[SchemaError]:
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
