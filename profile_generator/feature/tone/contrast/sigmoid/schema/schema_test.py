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

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "grey18": 87,
                "gamma": 1.7,
                "highlight_protection": True,
                "exposure_compensation": -1.0,
                "matte_effect": True,
            }
        )

    def test_validate_invalid_grey18(self) -> None:
        self.validator.assert_error(
            {"grey18": False},
            InvalidObjectError({"grey18": InvalidRangeError(16, 240)}),
        )

    def test_validate_invalid_gamma(self) -> None:
        self.validator.assert_error(
            {"gamma": False},
            InvalidObjectError({"gamma": InvalidRangeError(1.0, 5.0)}),
        )

    def test_validate_invalid_highlight_protection(self) -> None:
        self.validator.assert_error(
            {"highlight_protection": "invalid"},
            InvalidObjectError({"highlight_protection": InvalidTypeError(bool)}),
        )

    def test_validate_invalid_exposure_compensation(self) -> None:
        self.validator.assert_error(
            {"exposure_compensation": False},
            InvalidObjectError({"exposure_compensation": InvalidRangeError(-2.0, 2.0)}),
        )

    def test_validate_invalid_matte_effect(self) -> None:
        self.validator.assert_error(
            {"matte_effect": 0},
            InvalidObjectError({"matte_effect": InvalidTypeError(bool)}),
        )
