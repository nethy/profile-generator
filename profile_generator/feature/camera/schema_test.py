from unittest import TestCase

from profile_generator import ProfileParams
from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)
        self.profile_params = ProfileParams()

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"resolution_mp": 12.8})

    def test_validate_invalid_image_size(self) -> None:
        self.validator.assert_error(
            {"resolution_mp": -1.0},
            InvalidObjectError({"resolution_mp": InvalidRangeError(1.0, 1000.0)}),
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, {"SHRadius": "60", "LCRadius": "60"})

    def test_process_image_size(self) -> None:
        self.validator.assert_process(
            {"resolution_mp": 36}, {"SHRadius": "90", "LCRadius": "90"}
        )

    def test_parse(self) -> None:
        SCHEMA.parse({"resolution_mp": 36}, self.profile_params)

        self.assertEqual(self.profile_params.camera.resolution_mp, 36)
