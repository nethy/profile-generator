import unittest

from .range_schema import InvalidRangeError, range_of
from .schema_validator import SchemaValidator


class RangeSchemaTest(unittest.TestCase):
    def test_validate_int_range(self) -> None:
        schema = range_of(0, 100)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(0)
        validator.assert_valid(100)

        error = InvalidRangeError(0, 100)
        validator.assert_error(error, None)
        validator.assert_error(error, 0.0)
        validator.assert_error(error, False)
        validator.assert_error(error, "NaN")
        validator.assert_error(error, [])
        validator.assert_error(error, {})
        validator.assert_error(error, -1)
        validator.assert_error(error, 101)

    def test_validate_float_range(self) -> None:
        schema = range_of(0.0, 100.0)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(0.0)
        validator.assert_valid(100.0)
        validator.assert_valid(50)

        error = InvalidRangeError(0.0, 100.0)
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, "NaN")
        validator.assert_error(error, [])
        validator.assert_error(error, {})
        validator.assert_error(error, -1)
        validator.assert_error(error, 101)
