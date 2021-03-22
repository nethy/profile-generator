import unittest

from profile_generator.configuration.schema import (
    InvalidListError,
    InvalidListSizeError,
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_valid_config(self) -> None:
        self.validator.assert_valid(
            {"middle_grey": [128, 128], "strength": 25.1, "weights": [1.2, 1.2]}
        )

    def test_invalid_middle_grey(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"middle_grey": InvalidListSizeError(2)}),
            {"middle_grey": [128]},
        )
        self.validator.assert_error(
            InvalidObjectError(
                {"middle_grey": InvalidListError({1: InvalidRangeError(0, 255)})}
            ),
            {"middle_grey": [False, 128]},
        )

    def test_invalid_strength(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"strength": InvalidRangeError(0, 100)}),
            {"strength": False},
        )

    def test_invalid_weights(self) -> None:
        self.validator.assert_error(
            InvalidObjectError({"weights": InvalidListSizeError(2)}), {"weights": [1]}
        )

        self.validator.assert_error(
            InvalidObjectError(
                {"weights": InvalidListError({1: InvalidRangeError(0, 5)})}
            ),
            {"weights": [False, 0]},
        )
