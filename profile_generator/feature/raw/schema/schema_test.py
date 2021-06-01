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

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid({"demosaic": "RCD+VNG4"})
        self.validator.assert_valid({"demosaic": "LMMSE"})

    def test_validate_invalid_demosaic(self) -> None:
        self.validator.assert_error(
            {"demosaic": 1},
            InvalidObjectError({"demosaic": InvalidTypeError(str)}),
        )
        self.validator.assert_error(
            {"demosaic": "not_available"},
            InvalidObjectError({"demosaic": InvalidOptionError(("RCD+VNG4", "LMMSE"))}),
        )

    def test_process_default(self) -> None:
        self.validator.assert_process({}, {"BayerMethod": "dcbvng4"})

    def test_process_demosaic(self) -> None:
        self.validator.assert_process(
            {"demosaic": "DCB+VNG4"}, {"BayerMethod": "dcbvng4"}
        )

        self.validator.assert_process(
            {"demosaic": "dcb+vng4"}, {"BayerMethod": "dcbvng4"}
        )

        self.validator.assert_process({"demosaic": "LMMSE"}, {"BayerMethod": "lmmse"})
