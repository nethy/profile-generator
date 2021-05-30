import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidOptionError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_valid_config(self) -> None:
        self.validator.assert_valid({"demosaic": "RCD+VNG4"})
        self.validator.assert_valid({"demosaic": "LMMSE"})

    def test_invalid_demosaic(self) -> None:
        self.validator.assert_error(
            {"demosaic": 1},
            InvalidObjectError({"demosaic": InvalidTypeError(str)}),
        )
        self.validator.assert_error(
            {"demosaic": "not_available"},
            InvalidObjectError({"demosaic": InvalidOptionError(("RCD+VNG4", "LMMSE"))}),
        )
