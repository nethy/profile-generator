from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .grading import profile_generator_test as grading_test
from .profile_generator import generate

_DEFAULT = {
    "CCCurve": "0;",
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
                "CCCurve": "4;0.0000000;0.0000000;0.0313725;0.0401547;"
                + "0.0627451;0.0819951;0.0941176;0.1252106;"
                + "0.1215686;0.1638902;0.1490196;0.2031340;"
                + "0.1764706;0.2427041;0.2039216;0.2823626;"
                + "0.2313725;0.3218751;0.2588235;0.3610153;"
                + "0.2862745;0.3995681;0.3176471;0.4426527;"
                + "0.3490196;0.4844378;0.3803922;0.5246873;"
                + "0.4117647;0.5632035;0.4431373;0.5998301;"
                + "0.4784314;0.6386378;0.5137255;0.6748798;"
                + "0.5490196;0.7091215;0.5843137;0.7415203;"
                + "0.6235294;0.7753845;0.6627451;0.8070474;"
                + "0.7019608;0.8365711;0.7411765;0.8640295;"
                + "0.7843137;0.8919486;0.8274510;0.9175913;"
                + "0.8705882;0.9410857;0.9137255;0.9625636;"
                + "0.9568627;0.9821578;1.0000000;1.0000000;",
            },
        )
