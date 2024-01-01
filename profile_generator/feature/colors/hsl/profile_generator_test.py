from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {
    "LcEnabled": "false",
    "LcHhCurve": "0;",
    "LcChCurve": "0;",
    "LcLhCurve": "0;",
}


class ProfileGeneratorTest(TestCase):
    def test_process_default(self) -> None:
        self.assertEqual(generate(ProfileParams()), DEFAULT)

    def test_process_hue(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.hsl.parse({
            "hue": {
                "yellow": -5,
                "green": 5,
                "cyan": 0,
                "blue": 5,
                "magenta": -5,
            }
        })
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcEnabled": "true",
                "LcHhCurve": "1;0.0000000;0.5000000;0.0000000;0.0000000;"
                + "0.1666667;0.3750000;0.0000000;0.0000000;"
                + "0.3333333;0.6250000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.6250000;0.0000000;0.0000000;"
                + "0.8333333;0.3750000;0.0000000;0.0000000;",
            },
        )

    def test_process_saturation(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.hsl.parse({
            "saturation": {
                "red": 5,
                "magenta": -5,
            }
        })
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcEnabled": "true",
                "LcChCurve": "1;0.0000000;0.6500000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.3500000;0.0000000;0.0000000;",
            },
        )

    def test_process_luminances(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.hsl.parse({
            "luminance": {
                "red": 5,
                "magenta": -5,
            }
        })
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcEnabled": "true",
                "LcLhCurve": "1;0.0000000;0.5350000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.4650000;0.0000000;0.0000000;",
            },
        )
