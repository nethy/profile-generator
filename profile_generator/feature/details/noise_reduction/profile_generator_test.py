from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

_DEFAULT = {
    "DenoiseEnabled": "false",
    "DenoiseSMethod": "shal",
    "DenoiseLuma": "0",
    "DenoiseDetail": "100.0",
    "DenoiseChroma": "0",
    "ImpulseDenoiseEnabled": "false",
}


class ProfileGeneratorTest(TestCase):
    def test_generate_default(self) -> None:
        self.assertEqual(
            generate(ProfileParams()),
            _DEFAULT,
        )

    def test_generate_luminance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse(
            {"details": {"noise_reduction": {"luminance": 40, "detail": 50}}}
        )
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "DenoiseEnabled": "true",
                "DenoiseLuma": "40",
                "DenoiseDetail": "50",
            },
        )

    def test_generate_chrominance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"details": {"noise_reduction": {"chrominance": 40}}})
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "DenoiseEnabled": "true",
                "DenoiseChroma": "40",
            },
        )

    def test_generate_mode(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"details": {"noise_reduction": {"mode": "conservative"}}})
        self.assertEqual(
            generate(profile_params),
            {**_DEFAULT, "DenoiseSMethod": "shal"},
        )

        profile_params = ProfileParams()
        profile_params.parse(
            {"details": {"noise_reduction": {"mode": "aggressive", "luminance": 20}}}
        )
        self.assertEqual(
            generate(profile_params),
            {
                **_DEFAULT,
                "DenoiseSMethod": "shalbi",
                "ImpulseDenoiseEnabled": "true",
                "DenoiseEnabled": "true",
                "DenoiseLuma": "20",
            },
        )
