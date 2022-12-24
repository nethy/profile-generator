from unittest import TestCase

from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    SchemaValidator,
)

from .grading import schema_test as grading_test
from .hsl import schema_test as hsl_test
from .schema import SCHEMA
from .space import schema_test as profile_test
from .white_balance import schema_test as wb_test

_DEFAULT = {
    "Chromaticity": "0",
    **wb_test.DEFAULT,
    **hsl_test.DEFAULT,
    **profile_test.DEFAULT,
    **grading_test.DEFAULT,
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"vibrance": 5})

    def test_validate_invalid_vibrance(self) -> None:
        self.validator.assert_error(
            {"vibrance": False},
            InvalidObjectError({"vibrance": InvalidRangeError(0, 10)}),
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)

    def test_process_vibrance(self) -> None:
        self.validator.assert_process({"vibrance": 0}, _DEFAULT)

        self.validator.assert_process(
            {"vibrance": 5},
            _DEFAULT | {"Chromaticity": "25"},
        )
