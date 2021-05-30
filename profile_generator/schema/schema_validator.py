import unittest
from collections.abc import Mapping
from typing import Any

from .schema import Schema, SchemaError


class SchemaValidator:
    def __init__(self, assertions: unittest.TestCase, schema: Schema):
        self.assertions = assertions
        self.schema = schema

    def assert_valid(self, data: Any) -> None:
        self.assertions.assertIsNone(self.schema.validate(data))

    def assert_invalid(self, data: Any) -> None:
        error = self.schema.validate(data)
        self.assertions.assertIsNotNone(error)

    def assert_error(self, data: Any, error: SchemaError) -> None:
        self.assertions.assertEqual(self.schema.validate(data), error)

    def assert_process(self, data: Any, expectation: Mapping[str, str]) -> None:
        actual = self.schema.process(data)
        self.assertions.assertEqual(actual, expectation)
