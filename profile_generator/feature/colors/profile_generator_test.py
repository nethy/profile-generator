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
        self.assertEqual(generate(ProfileParams(), False), _DEFAULT)

    def test_generate_vibrance(self) -> None:
        profile_params = ProfileParams()
        profile_params.parse({"colors": {"vibrance": 5}})

        self.assertEqual(
            generate(profile_params, False),
            _DEFAULT
            | {
                "LCEnabled": "true",
                "CCCurve": "4;0.0000000;0.0000000;0.0313725;0.0397615;"
                + "0.0627451;0.0803531;0.0941176;0.1214170;0.1254902;0.1626383;"
                + "0.1568627;0.2037420;0.1882353;0.2444901;0.2196078;0.2846790;"
                + "0.2509804;0.3241372;0.2823529;0.3627229;0.3137255;0.4003220;"
                + "0.3450980;0.4368467;0.3764706;0.4722329;0.4117647;0.5106313;"
                + "0.4470588;0.5475107;0.4823529;0.5828757;0.5176471;0.6168224;"
                + "0.5529412;0.6497696;0.5882353;0.6818182;0.6235294;0.7130045;"
                + "0.6627451;0.7466863;0.7019608;0.7793904;0.7411765;0.8111588;"
                + "0.7803922;0.8420310;0.8196078;0.8720445;0.8588235;0.9012346;"
                + "0.8980392;0.9296346;0.9372549;0.9572764;0.9764706;0.9841897;"
                + "1.0000000;1.0000000;",
            },
        )
