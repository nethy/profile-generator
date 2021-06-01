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
                "LabaCurve": "1;0.000000;0.000000;0.125490;0.083398;0.305882;0.257195;"
                + "0.768627;0.822289;0.909804;0.943055;1.000000;1.000000;",
                "LabbCurve": "1;0.000000;0.000000;0.125490;0.083398;0.305882;0.257195;"
                + "0.768627;0.822289;0.909804;0.943055;1.000000;1.000000;",
            },
        )

        self.validator.assert_process(
            {"vibrance": -50},
            {
                "LabEnabled": "true",
                "LabaCurve": "1;0.000000;0.119203;1.000000;0.880797;",
                "LabbCurve": "1;0.000000;0.119203;1.000000;0.880797;",
            },
        )
