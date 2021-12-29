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
        self.validator.assert_valid({"local": 5})

    def test_validate_invalid_local(self) -> None:
        self.validator.assert_error(
            {"local": -1}, InvalidObjectError({"local": InvalidRangeError(0, 10)})
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {},
            {
                "WaveletEnabled": "false",
                "WaveletOpacityCurveWL": "1;0.150000;0.500000;0.000000;0.000000;"
                + "0.350000;0.500000;0.000000;0.000000;"
                + "0.650000;0.500000;0.000000;0.000000;"
                + "0.850000;0.500000;0.000000;0.000000;",
            },
        )

    def test_process_local(self) -> None:
        self.validator.assert_process(
            {"local": 1},
            {
                "WaveletEnabled": "true",
                "WaveletOpacityCurveWL": "1;0.150000;0.500000;0.000000;0.000000;"
                + "0.350000;0.550000;0.000000;0.000000;"
                + "0.650000;0.550000;0.000000;0.000000;"
                + "0.850000;0.500000;0.000000;0.000000;",
            },
        )
        self.validator.assert_process(
            {"local": 10},
            {
                "WaveletEnabled": "true",
                "WaveletOpacityCurveWL": "1;0.150000;0.500000;0.000000;0.000000;"
                + "0.350000;1.000000;0.000000;0.000000;"
                + "0.650000;1.000000;0.000000;0.000000;"
                + "0.850000;0.500000;0.000000;0.000000;",
            },
        )
