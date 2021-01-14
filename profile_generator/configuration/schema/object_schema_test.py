import unittest

from .object_schema import (
    InvalidObjectError,
    InvalidTypeError,
    UnkownMemberError,
    object_of,
)
from .schema_validator import SchemaValidator
from .type_schema import type_of


class ObjectSchemaTest(unittest.TestCase):
    def test_validate_object(self) -> None:
        schema = object_of(a=type_of(bool))
        validator = SchemaValidator(self, schema)

        validator.assert_valid({"a": True})
        validator.assert_valid({})

        error = InvalidTypeError(dict)
        validator.assert_error(error, None)
        validator.assert_error(error, [])
        validator.assert_error(error, 0)

        validator.assert_error(
            InvalidObjectError({"a": InvalidTypeError(bool)}), {"a": None}
        )
        validator.assert_error(
            InvalidObjectError({"a": InvalidTypeError(bool), "b": UnkownMemberError()}),
            {"a": 0, "b": False},
        )
        validator.assert_error(
            InvalidObjectError({"b": UnkownMemberError(), "a": InvalidTypeError(bool)}),
            {"b": False, "a": 0},
        )

    def test_validate_dot_notation(self) -> None:
        schema = object_of(a=object_of(b=type_of(bool)))
        validator = SchemaValidator(self, schema)

        validator.assert_valid({"a": {"b": True}})
        validator.assert_valid({"a.b": True})

        validator.assert_error(
            InvalidObjectError({"c": UnkownMemberError()}), {"c.b": True}
        )
        validator.assert_error(
            InvalidObjectError({"a": InvalidObjectError({"c": UnkownMemberError()})}),
            {"a.c": True},
        )
        validator.assert_error(
            InvalidObjectError(
                {"a": InvalidObjectError({"b": InvalidTypeError(bool)})}
            ),
            {"a.b": 0},
        )
