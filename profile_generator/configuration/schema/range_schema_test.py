import unittest

from .range_schema import InvalidRangeError, range_of
from .schema_validator import SchemaValidator


class RangeSchemaTest(unittest.TestCase):
    def test_validate_range(self) -> None:
        schema = range_of(0, 100)
        validator = SchemaValidator(self, schema)

        validator.assert_valid(0)
        validator.assert_valid(100)

        error = InvalidRangeError(0, 100)
        validator.assert_errors([error], None)
        validator.assert_errors([error], 0.0)
        validator.assert_errors([error], False)
        validator.assert_errors([error], "NaN")
        validator.assert_errors([error], [])
        validator.assert_errors([error], {})
        validator.assert_errors([error], -1)
        validator.assert_errors([error], 101)
