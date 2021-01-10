import unittest

from .schema_validator import SchemaValidator
from .type_schema import InvalidTypeError, type_of


class TypeSchemaTest(unittest.TestCase):
    def test_validate_bool(self) -> None:
        schema = type_of(bool)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(True)
        validator.assert_valid(False)

        error = InvalidTypeError(bool)
        validator.assert_error(error, 0)
        validator.assert_error(error, 1.0)
        validator.assert_error(error, "NaN")
        validator.assert_error(error, [])
        validator.assert_error(error, {})

    def test_validate_int(self) -> None:
        schema = type_of(int)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(1)
        validator.assert_valid(-1)

        error = InvalidTypeError(int)
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, 1.0)
        validator.assert_error(error, "NaN")
        validator.assert_error(error, [])
        validator.assert_error(error, {})

    def test_validate_float(self) -> None:
        schema = type_of(float)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(1.0)
        validator.assert_valid(1)

        error = InvalidTypeError(float)
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, "NaN")
        validator.assert_error(error, [])
        validator.assert_error(error, {})

    def test_validate_str(self) -> None:
        schema = type_of(str)
        validator = SchemaValidator(self, schema)

        validator.assert_valid("")

        error = InvalidTypeError(str)
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, 0)
        validator.assert_error(error, 1.0)
        validator.assert_error(error, [])
        validator.assert_error(error, {})
