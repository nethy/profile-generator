import re
import unittest

from util import file

from . import marshaller


class MarshallerTest(unittest.TestCase):
    def test_marshal_completeness(self) -> None:
        template_path = file.get_full_path("templates", "raw_therapee.pp3")
        with open(template_path, "rt") as reader:
            template = reader.read()
        placeholders = re.findall(r"\{(\w+)\}", template)

        result = marshaller.get_profile_args({})

        self.assertEqual(set(placeholders), set(result.keys()))
