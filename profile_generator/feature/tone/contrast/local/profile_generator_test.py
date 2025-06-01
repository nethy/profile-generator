from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate


class ProfileGeneratorTest(TestCase):
    def test_generate_defaults(self) -> None:
        self.assertEqual(
            generate(ProfileParams()),
            {
                "WaveletEnabled": "true",
                "WaveletContrast1": "14",
                "WaveletContrast2": "14",
            },
        )

    def test_generate_local_contrast(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"tone": {"curve": {"sigmoid": {"slope": 1.4}}}})
        self.assertEqual(
            generate(profile_params),
            {
                "WaveletEnabled": "true",
                "WaveletContrast1": "10",
                "WaveletContrast2": "10",
            },
        )
