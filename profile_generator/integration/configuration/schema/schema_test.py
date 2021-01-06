import unittest

from configuration.schema.schema_validator import SchemaValidator

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty(self) -> None:
        self.validator.assert_valid({})
        self.validator.assert_valid({"defaults": {}})
        self.validator.assert_valid({"templates": []})
        self.validator.assert_valid({"defaults": {}, "templates": []})

    def test_contrast_curve(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"contrast_bezier": {}}},
                "templates": [{"T": {"tone": {"contrast_bezier": {}}}}],
            }
        )
