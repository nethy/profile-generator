import unittest

from .options_schema import InvalidOptionError, InvalidTypeError, options_of
from .schema_validator import SchemaValidator


class OptionsSchemaTest(unittest.TestCase):
    def test_validate_options(self) -> None:
        schema = options_of("a", "B")
        validator = SchemaValidator(self, schema)

        validator.assert_valid("a")
        validator.assert_valid("b")
        validator.assert_valid("A")
        validator.assert_valid("B")

        error = InvalidTypeError(str)
        validator.assert_error(None, error)
        validator.assert_error(0, error)
        validator.assert_error(False, error)
        validator.assert_error([], error)
        validator.assert_error({}, error)

        validator.assert_error("", InvalidOptionError(("a", "B")))
        validator.assert_error("c", InvalidOptionError(("a", "B")))
