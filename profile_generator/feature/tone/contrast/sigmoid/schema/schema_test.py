from unittest import TestCase
from unittest.mock import Mock, patch

from profile_generator.feature.tone.contrast.sigmoid.schema import schema
from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)
from profile_generator.unit import Point

_CONTRAST_SIGMOID = (
    "profile_generator.feature.tone.contrast.sigmoid.schema.schema.contrast_sigmoid"
)
_CONTRAST_SIGMOID_GET_TONE_CURVE = f"{_CONTRAST_SIGMOID}.get_tone_curve"


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
            InvalidObjectError({"slope": InvalidRangeError(1.0, 4.0)}),
        )

    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    def test_process_default(self, get_tone_curve: Mock) -> None:
        get_tone_curve.return_value = [Point(0, 0)]

        self.validator.assert_process(
            {},
            {
                "Curve": "1;0.0000000;0.0000000;",
            },
        )
        get_tone_curve.assert_called_once_with(90.0 / 255, 1.6)
