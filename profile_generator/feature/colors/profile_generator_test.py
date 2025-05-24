from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .profile_generator import generate
from .space import profile_generator_test as profile_test
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "ColorAppEnabled": "true",
    "ColorAppChroma": "-2.4",
    **wb_test.DEFAULT,
    **grading_test.DEFAULT,
    **profile_test.DEFAULT,
    **grading_test.DEFAULT,
}


class ProfileGeneratorTest(TestCase):
    def test_generate_defaults(self) -> None:
        self.assertEqual(generate(ProfileParams()), _DEFAULT)

    def test_generate_vibrance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"colors": {"vibrance": 5}})
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "ColorAppChroma": "15.4",
            },
        )
