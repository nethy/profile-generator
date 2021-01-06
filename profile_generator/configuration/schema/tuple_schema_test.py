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
        validator.assert_errors([error], None)
        validator.assert_errors([error], False)
        validator.assert_errors([error], {})

        validator.assert_errors([InvalidListSizeError(2)], [False])
        validator.assert_errors([InvalidListSizeError(2)], [False, False, False])
        validator.assert_errors(
            [InvalidListError({2: InvalidTypeError(bool)})], [False, 0]
        )
        validator.assert_errors(
            [InvalidListError({1: InvalidTypeError(bool)})], [0, False]
        )
