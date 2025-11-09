from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

_DEFAULT = {"PDSEnabled": "false", "PDSDeconvRadius": "0.0", "PDSContrast": "10"}


class ProfileGeneratorTest(TestCase):
    def test_process_default(self) -> None:
        params = ProfileParams()
        params.parse({})

        self.assertEqual(generate(params, False), _DEFAULT)

    def test_process_radius(self) -> None:
        params = ProfileParams()
        params.details.sharpening.capture.parse({"radius": 0.7})

        self.assertEqual(
            generate(params, False),
            _DEFAULT | {"PDSEnabled": "true", "PDSDeconvRadius": "0.7"},
        )

        params = ProfileParams()
        params.details.sharpening.capture.parse({"radius": 0.39})

        self.assertEqual(
            generate(params, False),
            _DEFAULT,
        )

    def test_process_threshold(self) -> None:
        params = ProfileParams()
        params.details.sharpening.capture.parse({"threshold": 30})

        self.assertEqual(
            generate(params, False),
            _DEFAULT | {"PDSContrast": "30"},
        )
