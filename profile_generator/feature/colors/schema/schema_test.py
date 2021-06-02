from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA

_DEFAULT = {
    "LabEnabled": "false",
    "LabaCurve": "0;",
    "LabbCurve": "0;",
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

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)

    def test_process_vibrance(self) -> None:
        self.validator.assert_process(
            {"vibrance": 50},
            {
                "LabEnabled": "true",
                "LabaCurve": "1;0.000000;0.000000;0.113725;0.041165;0.313725;0.208478;"
                + "0.568627;0.618163;0.741176;0.853155;1.000000;1.000000;",
                "LabbCurve": "1;0.000000;0.000000;0.113725;0.041165;0.313725;0.208478;"
                + "0.568627;0.618163;0.741176;0.853155;1.000000;1.000000;",
            },
        )

        self.validator.assert_process(
            {"vibrance": -50},
            {
                "LabEnabled": "true",
                "LabaCurve": "1;0.000000;0.010163;1.000000;0.989837;",
                "LabbCurve": "1;0.000000;0.010163;1.000000;0.989837;",
            },
        )
