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
        self.validator.assert_process({}, {"LCEnabled": "false", "LCAmount": "0.0"})

    def test_process_local(self) -> None:
        self.validator.assert_process(
            {"local": 1},
            {"LCEnabled": "true", "LCAmount": "0.05"},
        )
        self.validator.assert_process(
            {"local": 10},
            {"LCEnabled": "true", "LCAmount": "0.5"},
        )
