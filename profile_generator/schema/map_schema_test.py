import unittest

from .map_schema import InvalidObjectError, InvalidTypeError, map_of
from .schema_validator import SchemaValidator
from .type_schema import type_of


class MapSchemaTest(unittest.TestCase):
    def test_validate_map(self) -> None:
        schema = map_of(type_of(bool))
        validator = SchemaValidator(self, schema)

        validator.assert_valid({"b": True})
        validator.assert_valid({})

        error = InvalidTypeError(dict)
        validator.assert_error(None, error)
        validator.assert_error("", error)

        validator.assert_error(
            {"a": None}, InvalidObjectError({"a": InvalidTypeError(bool)})
        )
        validator.assert_error(
            {"a": 0, "b": True}, InvalidObjectError({"a": InvalidTypeError(bool)})
        )
