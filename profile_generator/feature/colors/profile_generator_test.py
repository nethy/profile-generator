from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .hsl import profile_generator_test as hsl_test
from .profile_generator import generate
from .space import profile_generator_test as profile_test
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "VibranceEnabled": "true",
    "VibrancePastels": "15",
    "VibranceSaturated": "8",
    "ColorToningEnabled": "true",
    "ColorToningSaturation": "8",
    **wb_test.DEFAULT,
    **hsl_test.DEFAULT,
    **profile_test.DEFAULT,
    **grading_test.DEFAULT,
}


class ProfileGeneratorTest(TestCase):
    def test_process_defaults(self) -> None:
        self.assertEqual(generate(ProfileParams()), _DEFAULT)

    def test_process_vibrance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"colors": {"vibrance": 0}, "tone": {"curve": {"sigmoid": {"slope": 1}}}})
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "VibranceEnabled": "false",
                "VibrancePastels": "0",
                "VibranceSaturated": "0",
                "ColorToningEnabled": "false",
                "ColorToningSaturation": "0",
            },
        )

        profile_params = ProfileParams()
        profile_params.parse({"colors": {"vibrance": 5}, "tone": {"curve": {"sigmoid": {"slope": 1}}}})
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "VibrancePastels": "22",
                "VibranceSaturated": "11",
                "ColorToningSaturation": "11",
            },
        )

        profile_params = ProfileParams()
        profile_params.parse({"colors": {"vibrance": 0}, "tone": {"curve": {"sigmoid": {"slope": 1.4}}}})
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "VibrancePastels": "11",
                "VibranceSaturated": "5",
                "ColorToningSaturation": "5",
            },
        )
