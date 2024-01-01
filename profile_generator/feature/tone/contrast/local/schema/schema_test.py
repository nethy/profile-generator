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
                "DPEEnabled": "false",
                "DPEMult2": "1.0",
                "DPEMult3": "1.0",
                "DPEMult4": "1.0",
                "DPEMult5": "1.0",
            },
        )

    def test_process_local(self) -> None:
        self.validator.assert_process(
            {"local": 1},
            {
                "DPEEnabled": "true",
                "DPEMult2": "1.05",
                "DPEMult3": "1.1",
                "DPEMult4": "1.05",
                "DPEMult5": "1.025",
            },
        )
        self.validator.assert_process(
            {"local": 10},
            {
                "DPEEnabled": "true",
                "DPEMult2": "1.5",
                "DPEMult3": "2.0",
                "DPEMult4": "1.5",
                "DPEMult5": "1.25",
            },
        )
