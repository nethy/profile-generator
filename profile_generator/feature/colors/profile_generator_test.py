from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .profile_generator import generate
from .space import profile_generator_test as profile_test
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "LCEnabled": "false",
    "CCCurve": "0;",
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
                "LCEnabled": "true",
                "CCCurve": "4;0.0000000;0.0000000;0.0274510;0.0408926;"
                + "0.0549020;0.0812120;0.0823529;0.1209501;0.1098039;"
                + "0.1600982;0.1372549;0.1986472;0.1686275;0.2419576;"
                + "0.2000000;0.2844582;0.2313725;0.3261335;0.2627451;"
                + "0.3669668;0.2941176;0.4069402;0.3254902;0.4460349;"
                + "0.3568627;0.4842307;0.3882353;0.5215059;0.4196078;"
                + "0.5578371;0.4509804;0.5931992;0.4862745;0.6317891;"
                + "0.5215686;0.6690751;0.5568627;0.7050099;0.5921569;"
                + "0.7395408;0.6274510;0.7726080;0.6627451;0.8041438;"
                + "0.7019608;0.8372915;0.7411765;0.8683243;0.7803922;"
                + "0.8970866;0.8196078;0.9233828;0.8627451;0.9491499;"
                + "0.9058824;0.9711260;0.9529412;0.9897915;1.0000000;1.0000000;",
            },
        )
