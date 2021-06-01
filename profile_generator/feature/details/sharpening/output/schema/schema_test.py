import unittest
from typing import Any

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA

_DEFAULT = {
    "SharpeningEnabled": "false",
    "SharpeningContrast": "20",
    "DeconvRadius": "0.75",
    "DeconvAmount": "100",
    "DeconvDamping": "0",
    "DeconvIterations": "30",
}


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "enabled": True,
                "threshold": 50,
                "radius": 0.5,
                "amount": 50,
                "damping": 0,
                "iterations": 5,
            }
        )

    def test_validate_invalid_enabled(self) -> None:
        self.validator.assert_error(
            {"enabled": "false"},
            InvalidObjectError({"enabled": InvalidTypeError(bool)}),
        )

    def test_validate_invalid_threshold(self) -> None:
        self.validator.assert_error(
            {"threshold": "NaN"},
            InvalidObjectError({"threshold": InvalidRangeError(0, 200)}),
        )

    def test_validate_invalid_radius(self) -> None:
        self.validator.assert_error(
            {"radius": "NaN"},
            InvalidObjectError({"radius": InvalidRangeError(0.4, 2.5)}),
        )

    def test_validate_invalid_amount(self) -> None:
        self.validator.assert_error(
            {"amount": "NaN"}, InvalidObjectError({"amount": InvalidRangeError(0, 100)})
        )

    def test_validate_invalid_damping(self) -> None:
        self.validator.assert_error(
            {"damping": "NaN"},
            InvalidObjectError({"damping": InvalidRangeError(0, 100)}),
        )

    def test_validate_invalid_iterations(self) -> None:
        self.validator.assert_error(
            {"iterations": "NaN"},
            InvalidObjectError({"iterations": InvalidRangeError(5, 100)}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {},
            _DEFAULT,
        )

    def test_process_enabled(self) -> None:
        self._assert_process({"enabled": True}, SharpeningEnabled="true")
        self._assert_process({"enabled": False}, SharpeningEnabled="false")

    def test_process_threshold(self) -> None:
        self._assert_process({"threshold": 0}, SharpeningContrast="0")
        self._assert_process({"threshold": 200}, SharpeningContrast="200")

    def test_process_radius(self) -> None:
        self._assert_process({"radius": 0.4}, DeconvRadius="0.40")
        self._assert_process({"radius": 2.5}, DeconvRadius="2.50")

    def test_process_amount(self) -> None:
        self._assert_process({"amount": 0}, DeconvAmount="0")
        self._assert_process({"amount": 100}, DeconvAmount="100")

    def test_process_damping(self) -> None:
        self._assert_process({"damping": 0}, DeconvDamping="0")
        self._assert_process({"damping": 100}, DeconvDamping="100")

    def test_process_iterations(self) -> None:
        self._assert_process({"iterations": 5}, DeconvIterations="5")
        self._assert_process({"iterations": 100}, DeconvIterations="100")

    def _assert_process(self, data: Any, **expect_output: str) -> None:
        self.validator.assert_process(data, {**_DEFAULT, **expect_output})
