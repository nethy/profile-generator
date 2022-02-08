from unittest import TestCase

from profile_generator.schema import (
    InvalidListError,
    InvalidListSizeError,
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA, process

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

    def test_process_default(self) -> None:
        self.assertEqual(process({}), DEFAULT)

    def test_process(self) -> None:
        self.assertEqual(
            process(
                {
                    "shadow": [30, 5, -5],
                    "midtone": [120, 2, 0],
                    "highlight": [320, 8, 5],
                }
            ),
            {
                "RGBCurvesEnabled": "true",
                "RGBCurvesRCurve": "1;"
                + "0.000000;0.000000;"
                + "0.107703;0.121242;"
                + "0.189376;0.218222;"
                + "0.322696;0.337657;"
                + "0.466327;0.463372;"
                + "0.618420;0.632811;"
                + "0.777758;0.810620;"
                + "0.887567;0.904583;"
                + "1.000000;1.000000;",
                "RGBCurvesGCurve": "1;"
                + "0.000000;0.000000;"
                + "0.107703;0.103702;"
                + "0.189376;0.180557;"
                + "0.322696;0.318964;"
                + "0.466327;0.468206;"
                + "0.618420;0.612797;"
                + "0.777758;0.763749;"
                + "0.887567;0.880487;"
                + "1.000000;1.000000;",
                "RGBCurvesBCurve": "1;"
                + "0.000000;0.000000;"
                + "0.107703;0.101417;"
                + "0.189376;0.175756;"
                + "0.322696;0.309778;"
                + "0.466327;0.454658;"
                + "0.618420;0.630758;"
                + "0.777758;0.816269;"
                + "0.887567;0.907322;"
                + "1.000000;1.000000;",
            },
        )
