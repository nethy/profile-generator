from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

_DEFAULT = {"GrainEnabled": "false", "GrainStrength": "0"}


class ProfileGeneratorTest(TestCase):
    def test_generate_default(self) -> None:
        self.assertEqual(
            generate(ProfileParams()),
            _DEFAULT,
        )

    def test_generate_strength(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"details": {"grain": {"strength": 40}}})
        self.assertEqual(
            generate(profile_params),
            {"GrainEnabled": "true", "GrainStrength": "40"},
        )
