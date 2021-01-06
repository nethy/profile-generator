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
        validator.assert_errors([error], None)
        validator.assert_errors([error], [])
        validator.assert_errors([error], 0)

        validator.assert_errors(
            [InvalidObjectError({"a": InvalidTypeError(bool)})], {"a": None}
        )
        validator.assert_errors(
            [
                InvalidObjectError(
                    {"a": InvalidTypeError(bool), "b": UnkownMemberError()}
                )
            ],
            {"a": 0, "b": False},
        )
        validator.assert_errors(
            [
                InvalidObjectError(
                    {"b": UnkownMemberError(), "a": InvalidTypeError(bool)}
                )
            ],
            {"b": False, "a": 0},
        )
