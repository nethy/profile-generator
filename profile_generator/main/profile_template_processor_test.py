from unittest import TestCase

from .profile_template_processor import extract_partial

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


class ProfileTemplateProcessorTest(TestCase):
    def test_extract_partial_empty(self) -> None:
        self.assertEqual(extract_partial("", set()), "")
        self.assertEqual(extract_partial("", {"p2"}), "")
        self.assertEqual(extract_partial(_TEMPLATE, set()), "")

    def test_extract_partial(self) -> None:
        self.assertEqual(
            extract_partial(_TEMPLATE, {"p1"}),
            "\n".join(("[a]", "a2={p1}", "")),
        )
        self.assertEqual(
            extract_partial(_TEMPLATE, {"p2", "p1"}),
            "\n".join(("[a]", "a2={p1}", "", "[C]", "c1={p2}", "")),
        )
