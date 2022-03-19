import unittest
from collections.abc import Mapping
from typing import Any

from .object_schema import (
    InvalidObjectError,
    InvalidTypeError,
    ProfileInput,
    UnkownMemberError,
    object_of,
)
from .schema_validator import SchemaValidator
from .type_schema import type_of


def _test_parse(data: Any, profile_input: ProfileInput) -> None:
    profile_input.camera.resolution_mp = data["test"]


_PARSE_SCHEMA = object_of({"test": type_of(int)}, parser=_test_parse)


class ObjectSchemaTest(unittest.TestCase):
    def test_validate_object(self) -> None:
        schema = object_of({"a": type_of(bool)})
        validator = SchemaValidator(self, schema)

        validator.assert_valid({"a": True})
        validator.assert_valid({})

        error = InvalidTypeError(dict)
        validator.assert_error(None, error)
        validator.assert_error([], error)
        validator.assert_error(0, error)

        validator.assert_error(
            {"a": None}, InvalidObjectError({"a": InvalidTypeError(bool)})
        )
        validator.assert_error(
            {"a": 0, "b": False},
            InvalidObjectError({"a": InvalidTypeError(bool), "b": UnkownMemberError()}),
        )
        validator.assert_error(
            {"b": False, "a": 0},
            InvalidObjectError({"b": UnkownMemberError(), "a": InvalidTypeError(bool)}),
        )

    def test_process_object_with_processor(self) -> None:
        schema = object_of({"a": type_of(bool)}, ObjectSchemaTest._to_string)
        validator = SchemaValidator(self, schema)

        validator.assert_process({"a": True}, {"a": "True", "default": "_"})

    def test_process_object_without_processor(self) -> None:
        schema = object_of(
            {"a": object_of({"b": type_of(bool)}, ObjectSchemaTest._to_string)}
        )
        validator = SchemaValidator(self, schema)

        validator.assert_process({"a": {"b": False}}, {"b": "False", "default": "_"})

    def test_process_should_call_all_schemas(self) -> None:
        schema = object_of(
            {
                "a": object_of({"1": type_of(bool)}, ObjectSchemaTest._to_string),
                "b": object_of({"2": type_of(bool)}, ObjectSchemaTest._to_string),
            }
        )
        validator = SchemaValidator(self, schema)

        validator.assert_process({}, {"default": "_"})

    @staticmethod
    def _to_string(data: Any) -> Mapping[str, str]:
        return {key: str(value) for key, value in data.items()} | {"default": "_"}

    def test_parse_with_parser(self) -> None:
        profile_input = ProfileInput()

        _PARSE_SCHEMA.parse({"test": 2}, profile_input)

        self.assertEqual(profile_input.camera.resolution_mp, 2)

    def test_parse_object_without_parser(self) -> None:
        schema = object_of({"a": _PARSE_SCHEMA})
        profile_input = ProfileInput()

        schema.parse({"a": {"test": 2}}, profile_input)

        self.assertEqual(profile_input.camera.resolution_mp, 2)

    @staticmethod
    def _test_parse(data: Any, profile_input: ProfileInput) -> None:
        profile_input.camera.resolution_mp = data["test"]
