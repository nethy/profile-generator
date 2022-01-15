import unittest

from profile_generator.schema import SchemaValidator

from .demosaic import schema_test as demosaic_schema_test
from .schema import SCHEMA

_DEFAULT = demosaic_schema_test.DEFAULT


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_process_defaults(self) -> None:
        self.validator.assert_process({}, _DEFAULT)
