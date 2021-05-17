from typing import Any
from unittest import TestCase

from .configuration import create_from_template


class FactoryTest(TestCase):
    def test_empty_configs(self) -> None:
        self.assert_configurations({"Default": {}}, {})
        self.assert_configurations({"Default": {}}, {"templates": []})
        self.assert_configurations({"Default": {}}, {"defaults": {}})
        self.assert_configurations({"Default": {}}, {"defaults": {}, "templates": []})

    def test_creating_default_profile(self) -> None:
        self.assert_configurations({"Default": {"a": 1}}, {"defaults": {"a": 1}})

        self.assert_configurations(
            {"Default": {"a": 1}}, {"defaults": {"a": 1}, "templates": []}
        )

    def test_creating_profiles(self) -> None:
        self.assert_configurations(
            {"T1": {}, "T2": {}},
            {"templates": [{"optional": False, "settings": {"T1": {}, "T2": {}}}]},
        )

        self.assert_configurations(
            {"T": {"a": 1}},
            {"templates": [{"optional": False, "settings": {"T": {"a": 1}}}]},
        )

    def test_ignore_first_optional_template(self) -> None:
        self.assert_configurations(
            {"T": {"a": 1}},
            {"templates": [{"optional": True, "settings": {"T": {"a": 1}}}]},
        )

    def test_override_defaults_with_template(self) -> None:
        self.assert_configurations(
            {"T": {"a": 1, "b": 3, "c": 4}},
            {
                "defaults": {"a": 1, "b": 2},
                "templates": [{"optional": False, "settings": {"T": {"b": 3, "c": 4}}}],
            },
        )

        self.assert_configurations(
            {"T": {"nested": {"a": 1, "b": 3, "c": 4}}},
            {
                "defaults": {"nested": {"a": 1, "b": 2}},
                "templates": [
                    {"optional": False, "settings": {"T": {"nested": {"b": 3, "c": 4}}}}
                ],
            },
        )

    def test_override_multiple_templates(self) -> None:
        self.assert_configurations(
            {"T1_T2": {"a": 1, "b": 3, "c": 4}},
            {
                "templates": [
                    {"optional": False, "settings": {"T1": {"a": 1, "b": 2}}},
                    {"optional": False, "settings": {"T2": {"b": 3, "c": 4}}},
                ]
            },
        )

    def test_combining_templates(self) -> None:
        self.assert_configurations(
            {
                "T11_T21": {"a": 3},
                "T11_T22": {"a": 4},
                "T12_T21": {"a": 3},
                "T12_T22": {"a": 4},
            },
            {
                "templates": [
                    {
                        "optional": False,
                        "settings": {
                            "T11": {"a": 1},
                            "T12": {"a": 2},
                        },
                    },
                    {
                        "optional": False,
                        "settings": {
                            "T21": {"a": 3},
                            "T22": {"a": 4},
                        },
                    },
                ]
            },
        )

    def test_optional_templates(self) -> None:
        self.assert_configurations(
            {"T1": {"a": 1, "b": 2}, "T1_T2": {"a": 1, "b": 3, "c": 4}},
            {
                "templates": [
                    {"optional": False, "settings": {"T1": {"a": 1, "b": 2}}},
                    {"optional": True, "settings": {"T2": {"b": 3, "c": 4}}},
                ]
            },
        )

    def assert_configurations(
        self, expected: dict[str, dict[str, Any]], config: dict[str, Any]
    ) -> None:
        self.assertEqual(expected, create_from_template(config))
