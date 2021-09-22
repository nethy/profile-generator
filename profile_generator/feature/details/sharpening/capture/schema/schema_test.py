import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidOptionError,
    SchemaValidator,
)

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"type": "off"})

    def test_validate_invalid_type(self) -> None:
        self.validator.assert_error(
            {"type": "True"},
            InvalidObjectError(
                {"type": InvalidOptionError(("off", "aa", "no_aa", "muted"))}
            ),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process(
            {}, {"PDSEnabled": "false", "PDSDeconvRadius": "0.5"}
        )

    def test_process_type(self) -> None:
        self.validator.assert_process(
            {"type": "aa"},
            {"PDSEnabled": "true", "PDSDeconvRadius": "0.7"},
        )
        self.validator.assert_process(
            {"type": "no_aa"},
            {"PDSEnabled": "true", "PDSDeconvRadius": "0.59"},
        )
        self.validator.assert_process(
            {"type": "muted"},
            {"PDSEnabled": "true", "PDSDeconvRadius": "0.5"},
        )
