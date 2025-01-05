from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {
    "BayerMethod": "amaze",
    "BayerDDAutoContrast": "true",
    "BayerDDContrast": "20",
}


class ProfileGeneratorTest(TestCase):
    def test_generate_default(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.demosaic.parse({})
        self.assertEqual(
            generate(profile_params),
            DEFAULT,
        )

    def test_generate_algorithm(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.demosaic.parse({"algorithm": "rcd_vng4"})
        self.assertEqual(
            generate(profile_params), {**DEFAULT, "BayerMethod": "rcdvng4"}
        )

    def test_generate_auto_threshold(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.demosaic.parse({"auto_threshold": False})
        self.assertEqual(
            generate(profile_params), {**DEFAULT, "BayerDDAutoContrast": "false"}
        )

    def test_generate_threshold(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.demosaic.parse({"threshold": 50})
        self.assertEqual(generate(profile_params), {**DEFAULT, "BayerDDContrast": "50"})
