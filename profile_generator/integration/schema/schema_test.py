import re
import unittest

from profile_generator.schema.schema_validator import SchemaValidator
from profile_generator.util import file

from .schema import CONFIGURATION_SCHEMA, SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty(self) -> None:
        self.validator.assert_valid({})
        self.validator.assert_valid({"defaults": {}})
        self.validator.assert_valid({"templates": []})
        self.validator.assert_valid({"defaults": {}, "templates": []})

    def test_validate_tone_curve_bezier(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"curve": {"bezier": {}}}},
                "templates": [
                    {
                        "settings": {"T": {"tone": {"curve": {"bezier": {}}}}},
                    }
                ],
            }
        )

    def test_validate_tone_curve_sigmoid(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"curve": {"sigmoid": {}}}},
                "templates": [
                    {
                        "settings": {"T": {"tone": {"curve": {"sigmoid": {}}}}},
                    }
                ],
            }
        )

    def test_validate_tone_contrast(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"contrast": {}}},
                "templates": [{"settings": {"T": {"tone": {"contrast": {}}}}}],
            }
        )

    def test_validate_raw(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"raw": {}},
                "templates": [{"settings": {"T": {"raw": {}}}}],
            }
        )

    def test_validate_detials_enhance(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"enhance": {}}},
                "templates": [{"settings": {"T": {"details": {"enhance": {}}}}}],
            }
        )

    def test_validate_details_sharpening_capture(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"sharpening": {"capture": {}}}},
                "templates": [
                    {
                        "settings": {"T": {"details": {"sharpening": {"capture": {}}}}},
                    }
                ],
            }
        )

    def test_validate_details_sharpening_output(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"sharpening": {"output": {}}}},
                "templates": [
                    {
                        "settings": {"T": {"details": {"sharpening": {"output": {}}}}},
                    }
                ],
            }
        )

    def test_validate_details_noise_reduction(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"noise_reduction": {}}},
                "templates": [
                    {
                        "settings": {"T": {"details": {"noise_reduction": {}}}},
                    }
                ],
            }
        )

    def test_validate_colors(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"colors": {}},
                "templates": [{"settings": {"T": {"colors": {}}}}],
            }
        )

    def test_process_completeness(self) -> None:
        template_path = file.get_full_path("templates", "raw_therapee.pp3")
        with open(template_path, "rt") as reader:
            template = reader.read()
        placeholders = re.findall(r"\{(\w+)\}", template)

        result = CONFIGURATION_SCHEMA.process({})

        self.assertEqual(set(placeholders), set(result.keys()))
