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
        validator.assert_errors([error], None)
        validator.assert_errors([error], 0)
        validator.assert_errors([error], False)
        validator.assert_errors([error], [])
        validator.assert_errors([error], {})

        validator.assert_errors([InvalidOptionError(["a", "B"])], "")
        validator.assert_errors([InvalidOptionError(["a", "B"])], "c")
