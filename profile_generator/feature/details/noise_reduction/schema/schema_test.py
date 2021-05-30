import unittest

from profile_generator.schema import (
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
            {"mode": "not_available"},
            InvalidObjectError(
                {"mode": InvalidOptionError(("Conservative", "Aggressive"))}
            ),
        )

    def test_invalid_luminance(self) -> None:
        self.validator.assert_error(
            {"luminance": False},
            InvalidObjectError({"luminance": InvalidRangeError(0, 100)}),
        )

    def test_invalid_chrominance(self) -> None:
        self.validator.assert_error(
            {"chrominance": True},
            InvalidObjectError({"chrominance": InvalidRangeError(0, 100)}),
        )
