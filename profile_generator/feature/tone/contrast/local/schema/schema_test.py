from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"local": 50})

    def test_validate_invalid_local(self) -> None:
        self.validator.assert_error(
            {"local": -1}, InvalidObjectError({"local": InvalidRangeError(0, 100)})
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {}, {"WaveletEnabled": "false", "OpacityCurveWL": "0;"}
        )

    def test_process_local(self) -> None:
        self.validator.assert_process(
            {"local": 0},
            {"WaveletEnabled": "false", "OpacityCurveWL": "0;"},
        )
        self.validator.assert_process(
            {"local": 20},
            {
                "WaveletEnabled": "true",
                "OpacityCurveWL": (
                    "1;0.000000;0.500000;0.000000;0.146447;"
                    + "0.400000;0.600000;0.146447;0.000000;"
                    + "0.600000;0.600000;0.000000;0.146447;"
                    + "1.000000;0.500000;0.146447;0.000000;"
                ),
            },
        )
