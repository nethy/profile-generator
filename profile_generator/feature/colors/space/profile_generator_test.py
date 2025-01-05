from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {"CMWorkingProfile": "ProPhoto"}


class ProfileGeneratorTest(TestCase):
    def test_process_working(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.profile.parse({"working": "srgb"})
        self.assertEqual(generate(profile_params), {"CMWorkingProfile": "sRGB"})

        profile_params = ProfileParams()
        profile_params.colors.profile.parse({"working": "aCeSp1"})
        self.assertEqual(generate(profile_params), {"CMWorkingProfile": "ACESp1"})
