import unittest

from .schema_validator import SchemaValidator
from .tuple_schema import (
    InvalidListError,
    InvalidListSizeError,
    InvalidTypeError,
    tuple_of,
)
from .type_schema import type_of


class TupleSchemaTest(unittest.TestCase):
    def test_validate_tuple(self) -> None:
        schema = tuple_of(type_of(bool), type_of(bool))
        validator = SchemaValidator(self, schema)

        validator.assert_valid([True, False])

        error = InvalidTypeError(tuple)
        validator.assert_error(None, error)
        validator.assert_error(False, error)
        validator.assert_error({}, error)

        validator.assert_error([False], InvalidListSizeError(2))
        validator.assert_error([False, False, False], InvalidListSizeError(2))
        validator.assert_error(
            [False, 0], InvalidListError({2: InvalidTypeError(bool)})
        )
        validator.assert_error(
            [0, False], InvalidListError({1: InvalidTypeError(bool)})
        )
