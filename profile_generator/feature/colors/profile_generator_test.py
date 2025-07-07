from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .profile_generator import generate
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "LCEnabled": "false",
    "ACurve": "0;",
    "BCurve": "0;",
    "CTEnabled": "false",
    "CTPower": "1.0",
    "CTSaturation": "0",
    **wb_test.DEFAULT,
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
                "LCEnabled": "true",
                "ACurve": "4;0.0000000;0.0000000;0.1137255;0.0820368;"
                + "0.3333333;0.2857143;0.4627451;0.4461248;0.5568627;"
                + "0.5807050;0.7254902;0.7760000;0.9058824;0.9330544;"
                + "1.0000000;1.0000000;",
                "BCurve": "4;0.0000000;0.0000000;0.1137255;0.0820368;"
                + "0.3333333;0.2857143;0.4627451;0.4461248;0.5568627;"
                + "0.5807050;0.7254902;0.7760000;0.9058824;0.9330544;"
                + "1.0000000;1.0000000;",
            },
        )
