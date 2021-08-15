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
        self.validator.assert_valid({"image_size_in_mp": 12.8})

    def test_validate_invalid_image_size(self) -> None:
        self.validator.assert_error(
            {"image_size_in_mp": -1.0},
            InvalidObjectError({"image_size_in_mp": InvalidRangeError(1.0, 1000.0)}),
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, {"SHRadius": "40"})

    def test_process_image_size(self) -> None:
        self.validator.assert_process({"image_size_in_mp": 49}, {"SHRadius": "70"})
