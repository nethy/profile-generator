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

    def test_validate_config(self) -> None:
        self.validator.assert_valid({"strength": 100})

    def test_validate_invalid_strength(self) -> None:
        self.validator.assert_error(
            {"strength": False},
            InvalidObjectError({"strength": InvalidRangeError(0, 100)}),
        )
