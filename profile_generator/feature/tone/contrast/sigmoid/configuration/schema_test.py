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
        self.validator.assert_valid(
            {
                "grey": {"x": 128, "y": 128},
                "strength": 25.1,
                "protect_hl": True,
                "matte_effect": True,
            }
        )

    def test_invalid_middle_grey(self) -> None:
        self.validator.assert_error(
            InvalidObjectError(
                {"grey": InvalidObjectError({"x": InvalidRangeError(16, 240)})}
            ),
            {"grey": {"x": False}},
        )

        self.validator.assert_error(
            InvalidObjectError(
                {"grey": InvalidObjectError({"y": InvalidRangeError(64, 192)})}
            ),
            {"grey": {"y": False}},
        )

    def test_invalid_strength(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"strength": InvalidRangeError(0.0, 100.0)}),
            {"strength": False},
        )

    def test_invalid_hl_protect(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"protect_hl": InvalidTypeError(bool)}),
            {"protect_hl": 0},
        )

    def test_invalid_matte_effect(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"matte_effect": InvalidTypeError(bool)}),
            {"matte_effect": 0},
        )
