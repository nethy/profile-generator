from unittest import TestCase

from .dot_notation import expand


class DotNotationTest(TestCase):
    def test_expand_keeps_dotless_keys(self) -> None:
        self.assertEqual({}, expand({}))
        self.assertEqual({"a": 1}, expand({"a": 1}))
        self.assertEqual({"a": {"b": 1}}, expand({"a": {"b": 1}}))

    def test_expand_splits_keys_by_dots(self) -> None:
        self.assertEqual({"a": {"b": 1}}, expand({"a.b": 1}))
        self.assertEqual({"a": {"b": {"c": 1}}}, expand({"a.b.c": 1}))
        self.assertEqual(
            {"a": {"b": {"c": 1, "d": 2}}},
            expand({"a.b": {"c": 1, "d": 2}}),
        )
        self.assertEqual({"a": {"b": {"c": 1}}}, expand({"a": {"b.c": 1}}))

    def test_expand_merges_common_keys(self) -> None:
        self.assertEqual(
            {
                "a": {
                    "b": 1,
                    "c": 2,
                    "d": 3,
                }
            },
            expand({"a.b": 1, "a": {"c": 2, "d": 3}}),
        )

    def test_epand_list_items(self) -> None:
        self.assertEqual(
            [
                {"a": {"b": 1}},
                {"c": {"d": 2}},
            ],
            expand([{"a.b": 1}, {"c.d": 2}]),
        )

    def test_expand_list_in_dict(self) -> None:
        self.assertEqual({"a": [{"b": {"c": 1}}]}, expand({"a": [{"b.c": 1}]}))
