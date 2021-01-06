import unittest
from typing import Any, Dict

from .configuration import create_from_template


class FactoryTest(unittest.TestCase):
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
            {"T1": {}, "T2": {}}, {"templates": [{"T1": {}, "T2": {}}]}
        )

        self.assert_configurations({"T": {"a": 1}}, {"templates": [{"T": {"a": 1}}]})

    def test_override_defaults_with_template(self) -> None:
        self.assert_configurations(
            {"T": {"a": 1, "b": 3, "c": 4}},
            {"defaults": {"a": 1, "b": 2}, "templates": [{"T": {"b": 3, "c": 4}}]},
        )

        self.assert_configurations(
            {"T": {"nested": {"a": 1, "b": 3, "c": 4}}},
            {
                "defaults": {"nested": {"a": 1, "b": 2}},
                "templates": [{"T": {"nested": {"b": 3, "c": 4}}}],
            },
        )

    def test_override_multiple_templates(self) -> None:
        self.assert_configurations(
            {"T1-T2": {"a": 1, "b": 3, "c": 4}},
            {
                "templates": [
                    {"T1": {"a": 1, "b": 2}},
                    {"T2": {"b": 3, "c": 4}},
                ]
            },
        )

    def test_combining_templates(self) -> None:
        self.assert_configurations(
            {
                "T11-T21": {"a": 3},
                "T11-T22": {"a": 4},
                "T12-T21": {"a": 3},
                "T12-T22": {"a": 4},
            },
            {
                "templates": [
                    {
                        "T11": {"a": 1},
                        "T12": {"a": 2},
                    },
                    {
                        "T21": {"a": 3},
                        "T22": {"a": 4},
                    },
                ]
            },
        )

    def assert_configurations(
        self, expected: Dict[str, Dict[str, Any]], config: Dict[str, Any]
    ) -> None:
        self.assertEqual(expected, create_from_template(config))
