import unittest

from profile_generator.schema import InvalidListSizeError, SchemaValidator
from profile_generator.schema.object_schema import InvalidObjectError
from profile_generator.schema.type_schema import InvalidTypeError

from .demosaic import schema_test as demosaic_schema_test
from .schema import SCHEMA

_DEFAULT = {
    "BayerPreBlackRed": "0",
    "BayerPreBlackGreen": "0",
    "BayerPreBlackBlue": "0",
    **demosaic_schema_test.DEFAULT,
}
_BLACK_POINTS = "black_points"


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_invalid_black_points(self) -> None:
        self.validator.assert_error(
            {_BLACK_POINTS: False},
            InvalidObjectError({_BLACK_POINTS: InvalidTypeError(tuple)}),
        )
        self.validator.assert_error(
            {_BLACK_POINTS: [0, 0]},
            InvalidObjectError({_BLACK_POINTS: InvalidListSizeError(3)}),
        )

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)

    def test_process_black_points(self) -> None:
        self.validator.assert_process(
            {
                _BLACK_POINTS: [-1, 1, 2],
            },
            _DEFAULT
            | {
                "BayerPreBlackRed": "-1",
                "BayerPreBlackGreen": "1",
                "BayerPreBlackBlue": "2",
            },
        )
