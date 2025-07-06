from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .hsv import generate

DEFAULT = {
    "HSVEnabled": "false",
    "HSVHCurve": "0;",
    "HSVSCurve": "0;",
    "HSVVCurve": "0;",
}


class LchTest(TestCase):
    def test_generate_default(self) -> None:
        params = ProfileParams()
        params.parse({})

        self.assertDictEqual(generate(params), DEFAULT)

    def test_generate_hue(self) -> None:
        params = ProfileParams()
        params.parse(
            {
                "colors": {
                    "grading": {
                        "hsv": {
                            "hue": {
                                "yellow": 2,
                                "blue": -2,
                            }
                        }
                    }
                }
            }
        )

        self.assertDictEqual(
            generate(params),
            DEFAULT
            | {
                "HSVEnabled": "true",
                "HSVHCurve": "1;0.0208575;0.5118659;0.0000000;0.0000000;"
                + "0.0601268;0.5101878;0.0000000;0.0000000;"
                + "0.1122091;0.5085097;0.0000000;0.0000000;"
                + "0.1219933;0.5083333;0.0000000;0.0000000;"
                + "0.7019043;0.4916667;0.0000000;0.0000000;",
            },
        )
