from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA, process

DEFAULT = {
    "WBSetting": "Camera",
    "WBTemperature": "6504",
    "WBGreen": "1",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_invalid_wb_temperature(self) -> None:
        self.validator.assert_error(
            {"temperature": False},
            InvalidObjectError({"temperature": InvalidRangeError(1500, 60000)}),
        )

    def test_validate_invalid_wb_tint(self) -> None:
        self.validator.assert_error(
            {"tint": False}, InvalidObjectError({"tint": InvalidRangeError(0.02, 10.0)})
        )

    def test_process_wb_temperature(self) -> None:
        self.assertEqual(
            process({"temperature": 5500}),
            {**DEFAULT, "WBSetting": "Custom", "WBTemperature": "5500"},
        )

    def test_process_wb_tint(self) -> None:
        self.assertEqual(
            process({"tint": 0.880}),
            {**DEFAULT, "WBSetting": "Custom", "WBGreen": "0.88"},
        )
