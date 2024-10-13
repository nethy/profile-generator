import unittest

from profile_generator.schema import (
    InvalidObjectError,
    InvalidOptionError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA

DEFAULT = {
    "BayerMethod": "amaze",
    "BayerDDAutoContrast": "true",
    "BayerDDContrast": "20",
}


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {"algorithm": "RCD_VNG4", "auto_threshold": False, "threshold": 10}
        )

    def test_validate_invalid_algorithm(self) -> None:
        self.validator.assert_error(
            {"algorithm": 1},
            InvalidObjectError({"algorithm": InvalidTypeError(str)}),
        )
        self.validator.assert_error(
            {"algorithm": "not_available"},
            InvalidObjectError(
                {
                    "algorithm": InvalidOptionError(
                        (
                            "AMAZE",
                            "AMAZE_BILINEAR",
                            "AMAZE_VNG4",
                            "DCB_BILINEAR",
                            "DCB_VNG4",
                            "LMMSE",
                            "RCD_BILINEAR",
                            "RCD_VNG4",
                        )
                    )
                }
            ),
        )

    def test_validate_invalid_auto_threshold(self) -> None:
        self.validator.assert_error(
            {"auto_threshold": "false"},
            InvalidObjectError({"auto_threshold": InvalidTypeError(bool)}),
        )

    def test_validate_invalid_threshold(self) -> None:
        self.validator.assert_error(
            {"threshold": -1},
            InvalidObjectError({"threshold": InvalidRangeError(0, 100)}),
        )
