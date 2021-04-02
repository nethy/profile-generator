import unittest

from profile_generator.configuration.schema.schema_validator import SchemaValidator

from .schema import SCHEMA


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_empty(self) -> None:
        self.validator.assert_valid({})
        self.validator.assert_valid({"defaults": {}})
        self.validator.assert_valid({"templates": []})
        self.validator.assert_valid({"defaults": {}, "templates": []})

    def test_tone_contrast_bezier(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"curve": {"bezier": {}}}},
                "templates": [
                    {
                        "optional": False,
                        "settings": {"T": {"tone": {"curve": {"bezier": {}}}}},
                    }
                ],
            }
        )

    def test_tone_contrast(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"tone": {"contrast": {}}},
                "templates": [
                    {"optional": False, "settings": {"T": {"tone": {"contrast": {}}}}}
                ],
            }
        )

    def test_raw(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"raw": {}},
                "templates": [{"optional": False, "settings": {"T": {"raw": {}}}}],
            }
        )

    def test_details_sharpening_capture(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"sharpening": {"capture": {}}}},
                "templates": [
                    {
                        "optional": False,
                        "settings": {"T": {"details": {"sharpening": {"capture": {}}}}},
                    }
                ],
            }
        )

    def test_details_sharpening_output(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"sharpening": {"output": {}}}},
                "templates": [
                    {
                        "optional": False,
                        "settings": {"T": {"details": {"sharpening": {"output": {}}}}},
                    }
                ],
            }
        )

    def test_details_noise_reduction(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"details": {"noise_reduction": {}}},
                "templates": [
                    {
                        "optional": False,
                        "settings": {"T": {"details": {"noise_reduction": {}}}},
                    }
                ],
            }
        )

    def test_color(self) -> None:
        self.validator.assert_valid(
            {
                "defaults": {"colors": {}},
                "templates": [{"optional": False, "settings": {"T": {"colors": {}}}}],
            }
        )
