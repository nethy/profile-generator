import unittest

from profile_generator.configuration.schema import (
    InvalidObjectError,
    InvalidOptionError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_valid_config(self) -> None:
        self.validator.assert_valid(
            {"mode": "Aggressive", "luminance": 20, "chrominance": 30}
        )

    def test_invalid_mode(self) -> None:
        self.validator.assert_error(
            InvalidObjectError(
                {"mode": InvalidOptionError(("Conservative", "Aggressive"))}
            ),
            {"mode": "not_available"},
        )

    def test_invalid_luminance(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"luminance": InvalidRangeError(0, 100)}),
            {"luminance": False},
        )

    def test_invalid_chrominance(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"chrominance": InvalidRangeError(0, 100)}),
            {"chrominance": True},
        )
