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
_CONTRAST_SIGMOID_GET_FLAT = f"{_CONTRAST_SIGMOID}.get_flat"
_CONTRAST_SIGMOID_GET_CONTRAST = f"{_CONTRAST_SIGMOID}.get_contrast"


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, schema.SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "linear_grey18": 0.3,
                "slope": 1.7,
            }
        )

    def test_validate_invalid_grey18(self) -> None:
        self.validator.assert_error(
            {"linear_grey18": False},
            InvalidObjectError({"linear_grey18": InvalidRangeError(0.01, 0.75)}),
        )

    def test_validate_invalid_slope(self) -> None:
        self.validator.assert_error(
            {"slope": False},
            InvalidObjectError({"slope": InvalidRangeError(1.0, 4.0)}),
        )

    @patch(_CONTRAST_SIGMOID_GET_CONTRAST)
    @patch(_CONTRAST_SIGMOID_GET_FLAT)
    def test_process_default(self, get_flat: Mock, get_contrast: Mock) -> None:
        get_flat.return_value = [Point(1, 1)]
        get_contrast.return_value = [Point(1, 1)]

        self.validator.assert_process(
            {},
            {
                "Curve": "4;1.0000000;1.0000000;",
                "LCurve": "4;1.0000000;1.0000000;",
            },
        )
        get_flat.assert_called_once_with(0.1)
        get_contrast.assert_called_once_with(1.6)
