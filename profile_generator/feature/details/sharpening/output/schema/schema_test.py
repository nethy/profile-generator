import unittest

from profile_generator.schema import (
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
        self.validator.assert_valid(
            {
                "enabled": True,
                "threshold": 50,
                "radius": 0.5,
                "amount": 50,
                "damping": 0,
                "iterations": 5,
            }
        )

    def test_invalid_enabled(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"enabled": InvalidTypeError(bool)}),
            {"enabled": "false"},
        )

    def test_invalid_threshold(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"threshold": InvalidRangeError(0, 200)}),
            {"threshold": "NaN"},
        )

    def test_invalid_radius(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"radius": InvalidRangeError(0.4, 2.5)}),
            {"radius": "NaN"},
        )

    def test_invalid_amount(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"amount": InvalidRangeError(0, 100)}), {"amount": "NaN"}
        )

    def test_invalid_damping(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"damping": InvalidRangeError(0, 100)}),
            {"damping": "NaN"},
        )

    def test_invalid_iterations(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"iterations": InvalidRangeError(5, 100)}),
            {"iterations": "NaN"},
        )
