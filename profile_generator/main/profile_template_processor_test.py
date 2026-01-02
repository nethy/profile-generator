from pprint import pprint
from unittest import TestCase

from profile_generator.main import generator

from .profile_template_processor import get_partial_template, get_sections

_TEMPLATE = """
[a]
a1=0
a2={p1}

[b]
b1=0

[C]
c1={p2}
c2=0
"""

_SECTIONS = {"a": ["a2={p1}"], "C": ["c1={p2}"]}


class ProfileTemplateProcessorTest(TestCase):
    def test_get_partial_template_empty(self) -> None:
        self.assertEqual(get_partial_template("", set()), "")
        self.assertEqual(get_partial_template("", {"p2"}), "")
        self.assertEqual(get_partial_template(_TEMPLATE, set()), "")

    def test_get_partial_template(self) -> None:
        self.assertEqual(
            get_partial_template(_TEMPLATE, {"p1"}),
            "\n".join(("[a]", "a2={p1}", "")),
        )
        self.assertEqual(
            get_partial_template(_TEMPLATE, {"p2", "p1"}),
            "\n".join(("[a]", "a2={p1}", "", "[C]", "c1={p2}", "")),
        )

    def test_get_sections(self) -> None:
        self.assertEqual(get_sections(_TEMPLATE), _SECTIONS)
