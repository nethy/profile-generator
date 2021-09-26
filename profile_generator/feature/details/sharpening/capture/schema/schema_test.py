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
        self.validator.assert_valid({"radius": 0})

    def test_validate_invalid_radius(self) -> None:
        self.validator.assert_error(
            {"radius": "True"},
            InvalidObjectError({"radius": InvalidRangeError(0.0, 2.0)}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {}, {"PDSEnabled": "false", "PDSDeconvRadius": "0.0"}
        )

    def test_process_radius(self) -> None:
        self.validator.assert_process(
            {"radius": 0.7},
            {"PDSEnabled": "true", "PDSDeconvRadius": "0.7"},
        )
        self.validator.assert_process(
            {"radius": 0.39},
            {"PDSEnabled": "false", "PDSDeconvRadius": "0.0"},
        )
