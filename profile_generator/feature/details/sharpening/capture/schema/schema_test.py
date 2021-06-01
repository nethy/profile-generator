import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"enabled": False})

    def test_validate_invalid_enabled(self) -> None:
        self.validator.assert_error(
            {"enabled": "True"},
            InvalidObjectError({"enabled": InvalidTypeError(bool)}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process({}, {"PostDemosaicSharpeningEnabled": "false"})

    def test_process_enabled(self) -> None:
        self.validator.assert_process(
            {"enabled": True},
            {"PostDemosaicSharpeningEnabled": "true"},
        )
        self.validator.assert_process(
            {"enabled": False},
            {"PostDemosaicSharpeningEnabled": "false"},
        )
