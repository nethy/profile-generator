from unittest import TestCase

from profile_generator.schema import SchemaValidator
from profile_generator.schema.object_schema import InvalidObjectError
from profile_generator.schema.range_schema import InvalidRangeError

from .schema import SCHEMA


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_invalid_strength(self) -> None:
        self.validator.assert_error(
            {"strength": False},
            InvalidObjectError({"strength": InvalidRangeError(0, 5)}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {},
            {
                "DPEEnabled": "false",
                "DPEMult0": "1.0",
                "DPEMult1": "1.0",
                "DPEMult2": "1.0",
            },
        )

    def test_process_strength(self) -> None:
        self.validator.assert_process(
            {"strength": 3},
            {
                "DPEEnabled": "true",
                "DPEMult0": "1.3",
                "DPEMult1": "1.6",
                "DPEMult2": "1.3",
            },
        )
