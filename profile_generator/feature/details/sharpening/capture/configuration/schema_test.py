import unittest

from profile_generator.configuration.schema import (
    InvalidObjectError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_valid_config(self) -> None:
        self.validator.assert_valid({"enabled": False})

    def test_invalid_enabled(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"enabled": InvalidTypeError(bool)}),
            {"enabled": "True"},
        )
