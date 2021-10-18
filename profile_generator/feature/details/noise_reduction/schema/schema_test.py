import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidOptionError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA

_DEFAULT = {
    "DenoiseEnabled": "false",
    "DenoiseSMethod": "shal",
    "DenoiseLCurve": "0;",
    "DenoiseCCCurve": "0;",
    "ImpulseDenoiseEnabled": "false",
    "DPEEnabled": "false",
    "DPEMult1": "1.0",
}


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_config(self) -> None:
        self.validator.assert_valid(
            {"mode": "Aggressive", "luminance": 20, "chrominance": 30}
        )

    def test_validate_invalid_mode(self) -> None:
        self.validator.assert_error(
            {"mode": "not_available"},
            InvalidObjectError(
                {"mode": InvalidOptionError(("Conservative", "Aggressive"))}
            ),
        )

    def test_validate_invalid_luminance(self) -> None:
        self.validator.assert_error(
            {"luminance": False},
            InvalidObjectError({"luminance": InvalidRangeError(0, 100)}),
        )

    def test_validate_invalid_chrominance(self) -> None:
        self.validator.assert_error(
            {"chrominance": True},
            InvalidObjectError({"chrominance": InvalidRangeError(0, 100)}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {},
            _DEFAULT,
        )

    def test_luminance(self) -> None:
        self.validator.assert_process(
            {"luminance": 40},
            _DEFAULT
            | {
                "DenoiseEnabled": "true",
                "DenoiseLCurve": (
                    "1;0.000000;0.400000;0.000000;0.500000;"
                    + "1.000000;0.000000;0.000000;0.000000;"
                ),
                "DPEEnabled": "true",
                "DPEMult1": "1.8",
            },
        )

    def test_chrominance(self) -> None:
        self.validator.assert_process(
            {"chrominance": 40},
            _DEFAULT
            | {
                "DenoiseEnabled": "true",
                "DenoiseCCCurve": (
                    "1;0.000000;0.400000;0.000000;0.000000;"
                    + "0.333333;0.000000;0.500000;0.000000;"
                ),
            },
        )

    def test_mode(self) -> None:
        self.validator.assert_process(
            {"mode": "Conservative"},
            {**_DEFAULT, "DenoiseSMethod": "shal"},
        )

        self.validator.assert_process(
            {"mode": "Aggressive"},
            {**_DEFAULT, "DenoiseSMethod": "shalbi", "ImpulseDenoiseEnabled": "true"},
        )
