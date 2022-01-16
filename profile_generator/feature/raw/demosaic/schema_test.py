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
            {"algorithm": "RCD+VNG4", "auto_threshold": False, "threshold": 10}
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
                        ("AMaZE", "AMaZE+VNG4", "DCB+VNG4", "RCD+VNG4", "LMMSE")
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

    def test_process_default(self) -> None:
        self.validator.assert_process({}, DEFAULT)

    def test_process_algorithm(self) -> None:
        self.validator.assert_process(
            {"algorithm": "RCD+VNG4"}, DEFAULT | {"BayerMethod": "rcdvng4"}
        )

        self.validator.assert_process(
            {"algorithm": "rcd+vng4"}, DEFAULT | {"BayerMethod": "rcdvng4"}
        )

        self.validator.assert_process(
            {"algorithm": "LMMSE"}, DEFAULT | {"BayerMethod": "lmmse"}
        )

    def test_process_auto_threshold(self) -> None:
        self.validator.assert_process(
            {"auto_threshold": False}, DEFAULT | {"BayerDDAutoContrast": "false"}
        )

    def test_process_threshold(self) -> None:
        self.validator.assert_process(
            {"threshold": 50}, DEFAULT | {"BayerDDContrast": "50"}
        )
