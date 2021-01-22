import unittest

from profile_generator.configuration.schema import (
    InvalidObjectError,
    InvalidRangeError,
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
        self.validator.assert_valid({"enabled": True, "strength": 20, "median": False})

    def test_invalid_enabled(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"enabled": InvalidTypeError(bool)}), {"enabled": 1}
        )

    def test_invalid_strength(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"strength": InvalidRangeError(0, 100)}),
            {"strength": False},
        )

    def test_invalid_median(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"median": InvalidTypeError(bool)}), {"median": 0}
        )
