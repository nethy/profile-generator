from unittest import TestCase

from profile_generator.schema import SchemaValidator
from profile_generator.schema.object_schema import InvalidObjectError
from profile_generator.schema.options_schema import InvalidOptionError

from .schema import SCHEMA, process

DEFAULT = {"CMWorkingProfile": "ProPhoto"}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_invalid_working(self) -> None:
        self.validator.assert_error(
            {"working": "NotValid"},
            InvalidObjectError(
                {
                    "working": InvalidOptionError(
                        ("acesp0", "acesp1", "prophoto", "rec2020", "srgb")
                    )
                }
            ),
        )

    def test_process_working(self) -> None:
        self.assertEqual(process({"working": "srgb"}), {"CMWorkingProfile": "sRGB"})
        self.assertEqual(process({"working": "sRGB"}), {"CMWorkingProfile": "sRGB"})
