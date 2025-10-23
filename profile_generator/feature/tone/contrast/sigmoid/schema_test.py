from unittest import TestCase

from profile_generator.feature.tone.contrast.sigmoid import schema
from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, schema.SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "linear_grey18": 0.3,
                "slope": 1.7,
            }
        )

    def test_validate_invalid_grey18(self) -> None:
        self.validator.assert_error(
            {"linear_grey18": False},
            InvalidObjectError({"linear_grey18": InvalidRangeError(0.01, 0.75)}),
        )

    def test_validate_invalid_slope(self) -> None:
        self.validator.assert_error(
            {"slope": False},
            InvalidObjectError({"slope": InvalidRangeError(1.0, 4.0)}),
        )
