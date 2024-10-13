from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .hsl import profile_generator_test as hsl_test
from .profile_generator import generate
from .space import profile_generator_test as profile_test
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "LcACurve": "3;0.0000000;0.0000000;0.2853064;0.2146936;0.4500000;0.4500000;"
    + "0.5500000;0.5500000;0.7146936;0.7853064;1.0000000;1.0000000;",
    "LcBCurve": "3;0.0000000;0.0000000;0.2853064;0.2146936;0.4500000;0.4500000;"
    + "0.5500000;0.5500000;0.7146936;0.7853064;1.0000000;1.0000000;",
    **wb_test.DEFAULT,
    **hsl_test.DEFAULT,
    **profile_test.DEFAULT,
    **grading_test.DEFAULT,
}


class ProfileGeneratorTest(TestCase):
    def test_generate_defaults(self) -> None:
        self.assertEqual(generate(ProfileParams()), _DEFAULT)

    def test_generate_vibrance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse(
            {"colors": {"vibrance": 0}, "tone": {"curve": {"sigmoid": {"slope": 1}}}}
        )
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "LcACurve": "3;0.0000000;0.0000000;"
                + "0.2500000;0.2500000;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7500000;0.7500000;"
                + "1.0000000;1.0000000;",
                "LcBCurve": "3;0.0000000;0.0000000;"
                + "0.2500000;0.2500000;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7500000;0.7500000;"
                + "1.0000000;1.0000000;",
            },
        )

        profile_params = ProfileParams()
        profile_params.parse(
            {"colors": {"vibrance": 5}, "tone": {"curve": {"sigmoid": {"slope": 1}}}}
        )
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "LcACurve": "3;0.0000000;0.0000000;"
                + "0.3000000;0.2000000;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7000000;0.8000000;"
                + "1.0000000;1.0000000;",
                "LcBCurve": "3;0.0000000;0.0000000;"
                + "0.3000000;0.2000000;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7000000;0.8000000;"
                + "1.0000000;1.0000000;",
            },
        )

        profile_params = ProfileParams()
        profile_params.parse(
            {"colors": {"vibrance": 0}, "tone": {"curve": {"sigmoid": {"slope": 1.4}}}}
        )
        self.assertEqual(
            generate(profile_params),
            _DEFAULT
            | {
                "LcACurve": "3;0.0000000;0.0000000;"
                + "0.2753582;0.2246418;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7246418;0.7753582;"
                + "1.0000000;1.0000000;",
                "LcBCurve": "3;0.0000000;0.0000000;"
                + "0.2753582;0.2246418;0.4500000;0.4500000;"
                + "0.5500000;0.5500000;0.7246418;0.7753582;"
                + "1.0000000;1.0000000;",
            },
        )
