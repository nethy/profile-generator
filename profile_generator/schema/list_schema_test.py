import unittest

from .list_schema import InvalidListError, list_of
from .schema_validator import SchemaValidator
from .type_schema import InvalidTypeError, type_of


class ListSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = list_of(type_of(int))
        self.validator = SchemaValidator(self, self.schema)

    def test_validate_list(self) -> None:
        self.validator.assert_valid([])
        self.validator.assert_valid([0, 1])

        error = InvalidTypeError(list)
        self.validator.assert_error(None, error)
        self.validator.assert_error(False, error)
        self.validator.assert_error({}, error)

        self.validator.assert_error(
            [0, "NaN", None, 1],
            InvalidListError(
                {
                    2: InvalidTypeError(int),
                    3: InvalidTypeError(int),
                }
            ),
        )
