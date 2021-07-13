import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)
from profile_generator.schema.list_schema import InvalidListError
from profile_generator.schema.tuple_schema import InvalidListSizeError

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "neutral5": [87, 87, 87],
                "exposure_compensation": -1.0,
                "gamma": 1.7,
                "gain": {"shadow": 1.5, "highlight": 1.5},
                "matte_effect": True,
            }
        )

    def test_validate_invalid_neutral5(self) -> None:
        self.validator.assert_error(
            {"neutral5": [87, 87]},
            InvalidObjectError({"neutral5": InvalidListSizeError(3)}),
        )

        self.validator.assert_error(
            {"neutral5": [87, 87, False]},
            InvalidObjectError(
                {"neutral5": InvalidListError({3: InvalidRangeError(16, 240)})}
            ),
        )

    def test_validate_invalid_exposure_compensation(self) -> None:
        self.validator.assert_error(
            {"exposure_compensation": False},
            InvalidObjectError({"exposure_compensation": InvalidRangeError(-2.0, 2.0)}),
        )

    def test_validate_invalid_strength(self) -> None:
        self.validator.assert_error(
            {"gamma": False},
            InvalidObjectError({"gamma": InvalidRangeError(1.0, 5.0)}),
        )

    def test_validate_invalid_gain_shadow(self) -> None:
        self.validator.assert_error(
            {"gain": {"shadow": False}},
            InvalidObjectError(
                {"gain": InvalidObjectError({"shadow": InvalidRangeError(1.0, 4.0)})}
            ),
        )

    def test_validate_invalid_gain_highlight(self) -> None:
        self.validator.assert_error(
            {"gain": {"highlight": False}},
            InvalidObjectError(
                {"gain": InvalidObjectError({"highlight": InvalidRangeError(1.0, 4.0)})}
            ),
        )

    def test_validate_invalid_matte_effect(self) -> None:
        self.validator.assert_error(
            {"matte_effect": 0},
            InvalidObjectError({"matte_effect": InvalidTypeError(bool)}),
        )
