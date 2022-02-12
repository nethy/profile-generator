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
_CONTRAST_SIGMOID_FLAT = f"{_CONTRAST_SIGMOID}.flat"
_CONTRAST_SIGMOID_CONTRAST = f"{_CONTRAST_SIGMOID}.contrast"


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

    @patch(_CONTRAST_SIGMOID_CONTRAST)
    @patch(_CONTRAST_SIGMOID_FLAT)
    def test_process_default(self, flat: Mock, contrast: Mock) -> None:
        flat.return_value = [Point(0, 0)]
        contrast.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {},
            {
                "Curve": "1;0.000000;0.000000;",
                "Curve2": "1;1.000000;1.000000;",
                "CMToneCurve": "false",
                "CMApplyLookTable": "false",
            },
        )
        flat.assert_called_once_with(90.0 / 255)
        contrast.assert_called_once_with(90.0 / 255, 1.7)

    @patch(_CONTRAST_SIGMOID_CONTRAST)
    @patch(_CONTRAST_SIGMOID_FLAT)
    def test_process_linear_profile(self, flat: Mock, contrast: Mock) -> None:
        grey18 = 87
        slope = 1.5
        flat.return_value = [Point(0, 0)]
        contrast.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {"grey18": grey18, "slope": slope, "linear_profile": True},
            {
                "Curve": "1;0.000000;0.000000;",
                "Curve2": "1;1.000000;1.000000;",
                "CMToneCurve": "false",
                "CMApplyLookTable": "false",
            },
        )
        flat.assert_called_once_with(grey18 / 255)
        contrast.assert_called_once_with(grey18 / 255, slope)

    @patch(_CONTRAST_SIGMOID_CONTRAST)
    @patch(_CONTRAST_SIGMOID_FLAT)
    def test_process_nonlinear_profile(self, flat: Mock, contrast: Mock) -> None:
        grey18 = 87
        slope = 1.5
        flat.return_value = [Point(0, 0)]
        contrast.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {"grey18": grey18, "slope": slope, "linear_profile": False},
            {
                "Curve": "0;",
                "Curve2": "1;1.000000;1.000000;",
                "CMToneCurve": "true",
                "CMApplyLookTable": "true",
            },
        )
        flat.assert_not_called()
        contrast.assert_called_once_with(grey18 / 255, slope)
