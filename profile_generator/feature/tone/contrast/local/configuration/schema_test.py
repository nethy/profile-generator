from unittest import TestCase

from profile_generator.configuration.schema import SchemaValidator

from .schema import SCHEMA


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_valid_config(self) -> None:
        self.validator.assert_valid({"local": 50})

    def test_invalid_local(self) -> None:
        self.validator.assert_invalid({"local": -1})
