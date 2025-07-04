import unittest

from profile_generator.schema import InvalidListSizeError, SchemaValidator
from profile_generator.schema.object_schema import InvalidObjectError
from profile_generator.schema.type_schema import InvalidTypeError

from .schema import SCHEMA

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
