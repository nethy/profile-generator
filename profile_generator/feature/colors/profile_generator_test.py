from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .profile_generator import generate
from .white_balance import profile_generator_test as wb_test

_DEFAULT = {
    "LCEnabled": "false",
    "CCCurve": "0;",
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
                "CCCurve": "4;0.0000000;0.0000000;0.0274510;0.0406190;"
                + "0.0549020;0.0801527;0.0823529;0.1186441;0.1137255;0.1614100;"
                + "0.1450980;0.2029250;0.1764706;0.2432432;0.2078431;0.2824156;"
                + "0.2392157;0.3204904;0.2705882;0.3575130;0.3019608;0.3935264;"
                + "0.3333333;0.4285714;0.3686275;0.4668874;0.4039216;0.5040783;"
                + "0.4392157;0.5401929;0.4745098;0.5752773;0.5098039;0.6093750;"
                + "0.5450980;0.6425270;0.5803922;0.6747720;0.6156863;0.7061469;"
                + "0.6549020;0.7400295;0.6941176;0.7729258;0.7333333;0.8048780;"
                + "0.7725490;0.8359264;0.8117647;0.8661088;0.8509804;0.8954608;"
                + "0.8901961;0.9240163;0.9294118;0.9518072;0.9686275;0.9788639;"
                + "1.0000000;1.0000000;",
            },
        )
