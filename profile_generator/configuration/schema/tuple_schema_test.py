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
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, {})

        validator.assert_error(InvalidListSizeError(2), [False])
        validator.assert_error(InvalidListSizeError(2), [False, False, False])
        validator.assert_error(
            InvalidListError({2: InvalidTypeError(bool)}), [False, 0]
        )
        validator.assert_error(
            InvalidListError({1: InvalidTypeError(bool)}), [0, False]
        )
