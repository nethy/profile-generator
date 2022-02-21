from unittest import TestCase
from unittest.mock import Mock, patch

from profile_generator.feature.tone.contrast.sigmoid.schema import schema
from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)
from profile_generator.unit import Point

_CONTRAST_SIGMOID = (
    "profile_generator.feature.tone.contrast.sigmoid.schema.schema.contrast_sigmoid"
)
_CONTRAST_SIGMOID_COMPENSATE_SLOPE = f"{_CONTRAST_SIGMOID}.compensate_slope"
_CONTRAST_SIGMOID_GET_CONTRAST = f"{_CONTRAST_SIGMOID}.get_contrast"
_CONTRAST_SIGMOID_GET_TONE_CURVE = f"{_CONTRAST_SIGMOID}.get_tone_curve"
_CONTRAST_SIGMOID_GET_CHROMATICITY_CURVE = f"{_CONTRAST_SIGMOID}.get_chromaticity_curve"


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, schema.SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "grey18": 87,
                "slope": 1.7,
            }
        )

    def test_validate_invalid_grey18(self) -> None:
        self.validator.assert_error(
            {"grey18": False},
            InvalidObjectError({"grey18": InvalidRangeError(16, 240)}),
        )

    def test_validate_invalid_slope(self) -> None:
        self.validator.assert_error(
            {"slope": False},
            InvalidObjectError({"slope": InvalidRangeError(1.0, 5.0)}),
        )

    def test_validate_invalid_linear_profile(self) -> None:
        self.validator.assert_error(
            {"linear_profile": 1},
            InvalidObjectError({"linear_profile": InvalidTypeError(bool)}),
        )

    @patch(_CONTRAST_SIGMOID_GET_CHROMATICITY_CURVE)
    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    @patch(_CONTRAST_SIGMOID_COMPENSATE_SLOPE)
    def test_process_default(
        self, compensate_slope: Mock, get_tone_curve: Mock, get_chromaticity_curve: Mock
    ) -> None:
        compensate_slope.return_value = 2
        get_tone_curve.return_value = [Point(0, 0)]
        get_chromaticity_curve.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {},
            {
                "Curve": "2;0.176470588;0.352941176;0.676470588;0;0;0;0;",
                "LCurve": "1;0.0000000;0.0000000;",
                "ABCurve": "1;1.0000000;1.0000000;",
                "CMToneCurve": "false",
                "CMApplyLookTable": "false",
            },
        )
        compensate_slope.assert_called_once_with(90.0 / 255, 1.6)
        get_tone_curve.assert_called_once_with(90.0 / 255, 2)
        get_chromaticity_curve.assert_called_once_with(2)

    @patch(_CONTRAST_SIGMOID_GET_CHROMATICITY_CURVE)
    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    @patch(_CONTRAST_SIGMOID_COMPENSATE_SLOPE)
    def test_process_linear_profile(
        self, compensate_slope: Mock, get_tone_curve: Mock, get_chromaticity_curve: Mock
    ) -> None:
        grey18 = 87
        slope = 1.5
        compensate_slope.return_value = 2
        get_tone_curve.return_value = [Point(0, 0)]
        get_chromaticity_curve.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {"grey18": grey18, "slope": slope, "linear_profile": True},
            {
                "Curve": "2;0.170588235;0.341176471;0.670588235;0;0;0;0;",
                "LCurve": "1;0.0000000;0.0000000;",
                "ABCurve": "1;1.0000000;1.0000000;",
                "CMToneCurve": "false",
                "CMApplyLookTable": "false",
            },
        )
        compensate_slope.assert_called_once_with(grey18 / 255, slope)
        get_tone_curve.assert_called_once_with(grey18 / 255, 2)
        get_chromaticity_curve.assert_called_once_with(2)

    @patch(_CONTRAST_SIGMOID_GET_CHROMATICITY_CURVE)
    @patch(_CONTRAST_SIGMOID_GET_CONTRAST)
    @patch(_CONTRAST_SIGMOID_COMPENSATE_SLOPE)
    def test_process_nonlinear_profile(
        self, compensate_slope: Mock, get_contrast: Mock, get_chromaticity_curve: Mock
    ) -> None:
        grey18 = 87
        slope = 1.5
        compensate_slope.return_value = 2
        get_contrast.return_value = [Point(0, 0)]
        get_chromaticity_curve.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {"grey18": grey18, "slope": slope, "linear_profile": False},
            {
                "Curve": "2;0.230678065;0.46135613;0.730678065;0;0;0;0;",
                "LCurve": "1;0.0000000;0.0000000;",
                "ABCurve": "1;1.0000000;1.0000000;",
                "CMToneCurve": "true",
                "CMApplyLookTable": "true",
            },
        )
        compensate_slope.assert_called_once_with(grey18 / 255, slope)
        get_contrast.assert_called_once_with(2)
        get_chromaticity_curve.assert_called_once_with(2)
