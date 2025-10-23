import unittest

from profile_generator.schema import InvalidObjectError, SchemaValidator
from profile_generator.schema.range_schema import InvalidRangeError

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"radius": 0.5, "threshold": 50})

    def test_validate_invalid_radius(self) -> None:
        self.validator.assert_error(
            {"radius": "True"},
            InvalidObjectError({"radius": InvalidRangeError(0.0, 2.0)}),
        )

    def test_validate_invalid_threshold(self) -> None:
        self.validator.assert_error(
            {"threshold": False},
            InvalidObjectError({"threshold": InvalidRangeError(0, 200)}),
        )
