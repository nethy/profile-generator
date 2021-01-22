import unittest

from profile_generator.configuration.schema import (
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
            InvalidObjectError({"demosaic": InvalidTypeError(str)}),
            {"demosaic": 1},
        )
        self.validator.assert_error(
            InvalidObjectError({"demosaic": InvalidOptionError(["RCD+VNG4", "LMMSE"])}),
            {"demosaic": "not_available"},
        )
