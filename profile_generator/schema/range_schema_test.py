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
        validator.assert_error(None, error)
        validator.assert_error(0.0, error)
        validator.assert_error(False, error)
        validator.assert_error("NaN", error)
        validator.assert_error([], error)
        validator.assert_error({}, error)
        validator.assert_error(-1, error)
        validator.assert_error(101, error)

    def test_validate_float_range(self) -> None:
        schema = range_of(0.0, 100.0)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(0.0)
        validator.assert_valid(100.0)
        validator.assert_valid(50)

        error = InvalidRangeError(0.0, 100.0)
        validator.assert_error(None, error)
        validator.assert_error(False, error)
        validator.assert_error("NaN", error)
        validator.assert_error([], error)
        validator.assert_error({}, error)
        validator.assert_error(-1, error)
        validator.assert_error(101, error)
