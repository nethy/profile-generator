from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Optional

from profile_generator.profile_params import ProfileParams

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError

Processor = Callable[[Any], Mapping[str, str]]
Parser = Callable[[Any, ProfileParams], None]


class ObjectSchema(Schema):
    def __init__(
        self,
        object_schema: Mapping[str, Schema],
        processor: Optional[Processor] = None,
        parser: Optional[Parser] = None,
    ):
        self._object_schema = object_schema
        self._processor = processor
        self._parser = parser

    def validate(self, data: Any) -> Optional[SchemaError]:
        if not isinstance(data, dict):
            return InvalidTypeError(dict)

        return self._validate_object(data)

    def _validate_object(self, data: Any) -> Optional[SchemaError]:
        errors = self._collect_errors(data)

        if len(errors.keys()) > 0:
            return InvalidObjectError(errors)
        else:
            return None

    def _collect_errors(self, data: Any) -> Mapping[str, SchemaError]:
        errors: dict[str, SchemaError] = {}
        for name, value in data.items():
            error = self._get_member_error(name, value)
            if error is not None:
                errors[name] = error
        return errors

    def _get_member_error(self, name: str, value: Any) -> Optional[SchemaError]:
        if name not in self._object_schema:
            return UnkownMemberError()
        else:
            member_schema = self._object_schema.get(name, _ANY_SCHEMA)
            return member_schema.validate(value)

    def process(self, data: Any) -> Mapping[str, str]:
        if self._processor is not None:
            return self._processor(data)
        else:
            result: dict[str, str] = {}
            for member, schema in self._object_schema.items():
                config = data.get(member, {})
                partial_result = schema.process(config)
                result.update(partial_result)
            return result


class AnySchema(Schema):
    def validate(self, data: Any) -> Optional[SchemaError]:
        return None


_ANY_SCHEMA = AnySchema()


@dataclass
class InvalidObjectError(SchemaError):
    errors: Mapping[str, SchemaError]


@dataclass
class UnkownMemberError(SchemaError):
    ...


def object_of(
    object_schema: Mapping[str, Schema],
    processor: Optional[Processor] = None,
    parser: Optional[Parser] = None,
) -> Schema:
    return ObjectSchema(object_schema, processor, parser)
