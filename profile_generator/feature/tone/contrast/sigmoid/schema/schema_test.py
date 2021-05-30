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
                "grey": {"x": 128, "y": 128},
                "strength": 25.1,
                "protect_hl": True,
                "matte_effect": True,
            }
        )

    def test_invalid_middle_grey(self) -> None:
        self.validator.assert_error(
            {"grey": {"x": False}},
            InvalidObjectError(
                {"grey": InvalidObjectError({"x": InvalidRangeError(16, 240)})}
            ),
        )

        self.validator.assert_error(
            {"grey": {"y": False}},
            InvalidObjectError(
                {"grey": InvalidObjectError({"y": InvalidRangeError(64, 192)})}
            ),
        )

    def test_invalid_strength(self) -> None:
        self.validator.assert_error(
            {"strength": False},
            InvalidObjectError({"strength": InvalidRangeError(0.0, 100.0)}),
        )

    def test_invalid_hl_protect(self) -> None:
        self.validator.assert_error(
            {"protect_hl": 0},
            InvalidObjectError({"protect_hl": InvalidTypeError(bool)}),
        )

    def test_invalid_matte_effect(self) -> None:
        self.validator.assert_error(
            {"matte_effect": 0},
            InvalidObjectError({"matte_effect": InvalidTypeError(bool)}),
        )
