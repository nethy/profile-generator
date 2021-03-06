import unittest

from .list_schema import InvalidListError, list_of
from .schema_validator import SchemaValidator
from .type_schema import InvalidTypeError, type_of


class ListSchemaTest(unittest.TestCase):
    def test_validate_list(self) -> None:
        schema = list_of(type_of(int))
        validator = SchemaValidator(self, schema)

        validator.assert_valid([])
        validator.assert_valid([0, 1])

        error = InvalidTypeError(list)
        validator.assert_error(error, None)
        validator.assert_error(error, False)
        validator.assert_error(error, {})

        validator.assert_error(
            InvalidListError(
                {
                    2: InvalidTypeError(int),
                    3: InvalidTypeError(int),
                }
            ),
            [0, "NaN", None, 1],
        )
