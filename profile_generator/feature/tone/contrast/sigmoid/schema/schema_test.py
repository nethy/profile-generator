import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)
from profile_generator.schema.options_schema import InvalidOptionError

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "grey18": 87,
                "slope": 1.7,
                "brightness": -1.0,
            }
        )

    def test_validate_invalid_grey18(self) -> None:
        self.validator.assert_error(
            {"grey18": False},
            InvalidObjectError({"grey18": InvalidRangeError(16, 240)}),
        )

    def test_validate_invalid_slope(self) -> None:
        self.validator.assert_error(
            {"slope": False},
            InvalidObjectError({"slope": InvalidRangeError(1.0, 5.0)}),
        )

    def test_validate_invalid_brightness(self) -> None:
        self.validator.assert_error(
            {"brightness": False},
            InvalidObjectError({"brightness": InvalidRangeError(-2.0, 2.0)}),
        )

    def test_validate_invalid_highlight(self) -> None:
        self.validator.assert_error(
            {"highlight": "not_available"},
            InvalidObjectError({"highlight": InvalidOptionError(("soft", "strong"))}),
        )
