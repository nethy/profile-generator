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
            {"enabled": "false"},
            InvalidObjectError({"enabled": InvalidTypeError(bool)}),
        )

    def test_invalid_threshold(self) -> None:
        self.validator.assert_error(
            {"threshold": "NaN"},
            InvalidObjectError({"threshold": InvalidRangeError(0, 200)}),
        )

    def test_invalid_radius(self) -> None:
        self.validator.assert_error(
            {"radius": "NaN"},
            InvalidObjectError({"radius": InvalidRangeError(0.4, 2.5)}),
        )

    def test_invalid_amount(self) -> None:
        self.validator.assert_error(
            {"amount": "NaN"}, InvalidObjectError({"amount": InvalidRangeError(0, 100)})
        )

    def test_invalid_damping(self) -> None:
        self.validator.assert_error(
            {"damping": "NaN"},
            InvalidObjectError({"damping": InvalidRangeError(0, 100)}),
        )

    def test_invalid_iterations(self) -> None:
        self.validator.assert_error(
            {"iterations": "NaN"},
            InvalidObjectError({"iterations": InvalidRangeError(5, 100)}),
        )
