from unittest import TestCase

from profile_generator.schema import (
    InvalidListError,
    InvalidListSizeError,
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA

DEFAULT = {
    "RGBCurvesEnabled": "false",
    "RGBCurvesRCurve": "0;",
    "RGBCurvesGCurve": "0;",
    "RGBCurvesBCurve": "0;",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {"shadow": [30, 5, -5], "midtone": [120, 2, 0], "highlight": [320, 8, 5]}
        )

    def test_validate_invalid_shadow(self) -> None:
        self.validator.assert_error(
            {"shadow": False},
            InvalidObjectError({"shadow": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_midtone(self) -> None:
        self.validator.assert_error(
            {"midtone": False},
            InvalidObjectError({"midtone": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_highlight(self) -> None:
        self.validator.assert_error(
            {"highlight": False},
            InvalidObjectError({"highlight": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_tint_value(self) -> None:
        self.validator.assert_error(
            {"shadow": False}, InvalidObjectError({"shadow": InvalidTypeError(tuple)})
        )

        self.validator.assert_error(
            {"shadow": [0]},
            InvalidObjectError({"shadow": InvalidListSizeError(3)}),
        )

        self.validator.assert_error(
            {"shadow": [False, 0, 0]},
            InvalidObjectError(
                {"shadow": InvalidListError({1: InvalidRangeError(0.0, 360.0)})}
            ),
        )
