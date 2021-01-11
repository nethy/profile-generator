import unittest
from typing import Any

from .schema import Schema, SchemaError


class SchemaValidator:
    def __init__(self, assertions: unittest.TestCase, schema: Schema):
        self.assertions = assertions
        self.schema = schema

    def assert_valid(self, data: Any) -> None:
        self.assertions.assertEqual([], self.schema.validate(data))

    def assert_invalid(self, data: Any) -> None:
        errors = self.schema.validate(data)
        self.assertions.assertTrue(len(errors) > 0)

    def assert_error(self, error: SchemaError, data: Any) -> None:
        self.assertions.assertEqual([error], self.schema.validate(data))
