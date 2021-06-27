from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA

_DEFAULT = {
    "LabEnabled": "false",
    "LabChromacity": "0",
    "LabRASTProtection": "0",
    "WB_Setting": "Camera",
    "WB_Temperature": "6504",
    "WB_Green": "1",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"vibrance": 50})

    def test_validate_invalid_vibrance(self) -> None:
        self.validator.assert_error(
            {"vibrance": False},
            InvalidObjectError({"vibrance": InvalidRangeError(-100, 100)}),
        )

    def test_validate_invalid_skin_tone_protection(self) -> None:
        self.validator.assert_error(
            {"skin_tone_protection": False},
            InvalidObjectError({"skin_tone_protection": InvalidRangeError(0, 100)}),
        )

    def test_validate_invalid_wb_temperature(self) -> None:
        self.validator.assert_error(
            {"white_balance": {"temperature": False}},
            InvalidObjectError(
                {
                    "white_balance": InvalidObjectError(
                        {"temperature": InvalidRangeError(1500, 60000)}
                    )
                }
            ),
        )

    def test_validate_invalid_wb_tint(self) -> None:
        self.validator.assert_error(
            {"white_balance": {"tint": False}},
            InvalidObjectError(
                {
                    "white_balance": InvalidObjectError(
                        {"tint": InvalidRangeError(0.02, 10.0)}
                    )
                }
            ),
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)

    def test_process_vibrance(self) -> None:
        self.validator.assert_process(
            {"vibrance": 50},
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "LabChromacity": "50",
            },
        )

        self.validator.assert_process(
            {"vibrance": -50},
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "LabChromacity": "-50",
            },
        )

    def test_process_skin_tone_protection(self) -> None:
        self.validator.assert_process(
            {"skin_tone_protection": 50}, {**_DEFAULT, "LabRASTProtection": "50"}
        )

    def test_process_wb_temperature(self) -> None:
        self.validator.assert_process(
            {"white_balance": {"temperature": 5500}},
            {**_DEFAULT, "WB_Setting": "Custom", "WB_Temperature": "5500"},
        )

    def test_process_wb_tint(self) -> None:
        self.validator.assert_process(
            {"white_balance": {"tint": 0.880}},
            {**_DEFAULT, "WB_Setting": "Custom", "WB_Green": "0.88"},
        )
