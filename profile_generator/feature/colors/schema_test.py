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
    "HSVEnabled": "false",
    "HSVSCurve": "0;",
    "Chromaticity": "0",
    "CTEnabled": "false",
    "CTLabRegionPower": "1",
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
        self.validator.assert_valid({"vibrance": 5})

    def test_validate_invalid_vibrance(self) -> None:
        self.validator.assert_error(
            {"vibrance": False},
            InvalidObjectError({"vibrance": InvalidRangeError(-10, 10)}),
        )

    def test_validate_invalid_chrome(self) -> None:
        self.validator.assert_error(
            {"chrome": False}, InvalidObjectError({"chrome": InvalidRangeError(0, 10)})
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)

    def test_process_vibrance(self) -> None:
        self.validator.assert_process({"vibrance": 0}, _DEFAULT)

        self.validator.assert_process(
            {"vibrance": 5},
            {
                **_DEFAULT,
                "HSVEnabled": "true",
                "HSVSCurve": "1;0.041667;0.625000;0.25;0.25;"
                + "0.541667;0.750000;0.25;0.25;",
            },
        )

        self.validator.assert_process(
            {"vibrance": -5},
            {**_DEFAULT, "Chromaticity": "-50"},
        )

    def test_process_chrome(self) -> None:
        self.validator.assert_process({"chrome": 0}, _DEFAULT)

        self.validator.assert_process(
            {"chrome": 10}, _DEFAULT | {"CTEnabled": "true", "CTLabRegionPower": "2.0"}
        )
