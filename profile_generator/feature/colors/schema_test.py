from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .hsl import schema_test as hsl_schema_test
from .profile import schema_test as profile_test
from .schema import SCHEMA
from .white_balance import schema_test as wb_schema_test

_DEFAULT = {
    "LabEnabled": "false",
    "LabChromacity": "0",
    "LabRASTProtection": "0",
    **wb_schema_test.DEFAULT,
    **hsl_schema_test.DEFAULT,
    **profile_test.DEFAULT,
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
