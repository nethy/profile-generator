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
                "CCCurve": "4;0.0000000;0.0000000;0.0274510;0.0469294;"
                + "0.0549020;0.0917203;0.0823529;0.1344917;0.1098039;"
                + "0.1753591;0.1372549;0.2144347;0.1686275;0.2570380;"
                + "0.2000000;0.2976000;0.2313725;0.3362717;0.2627451;"
                + "0.3731986;0.2941176;0.4085200;0.3294118;0.4465039;"
                + "0.3647059;0.4828065;0.4000000;0.5176000;0.4352941;"
                + "0.5510474;0.4705882;0.5833024;0.5058824;0.6145092;"
                + "0.5450980;0.6481179;0.5843137;0.6807708;0.6235294;"
                + "0.7126252;0.6627451;0.7438246;0.7019608;0.7744980;"
                + "0.7411765;0.8047605;0.7803922;0.8347126;0.8196078;"
                + "0.8644411;0.8588235;0.8940183;0.8980392;0.9235024;"
                + "0.9372549;0.9529373;0.9764706;0.9823529;1.0000000;1.0000000;",
            },
        )
