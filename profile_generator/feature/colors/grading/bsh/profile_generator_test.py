from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {
    "LcHhCurve": "0;",
    "LcChCurve": "0;",
    "LcLhCurve": "0;",
}


class ProfileGeneratorTest(TestCase):
    def test_process_default(self) -> None:
        self.assertEqual(generate(ProfileParams()), DEFAULT)

    def test_process_brilliance(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.grading.bsh.parse(
            {
                "red": [5, 0, 0],
                "magenta": [-5, 0, 0]
            }
        )
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcLhCurve": "1;0.0000000;0.5350000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.4650000;0.0000000;0.0000000;",
            },
        )

    def test_process_saturation(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.grading.bsh.parse(
            {
                "red": [0, 5, 0],
                "magenta": [0, -5, 0],
            }
        )
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcChCurve": "1;0.0000000;0.6500000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.3500000;0.0000000;0.0000000;",
            },
        )

    def test_process_hue(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.grading.bsh.parse(
            {
                "yellow": [0, 0, -5],
                "green": [0, 0, 5],
                "cyan": [0, 0, 0],
                "blue": [0, 0, 5],
                "magenta": [0, 0, -5],
            }
        )
        self.assertEqual(
            generate(profile_params),
            DEFAULT
            | {
                "LcHhCurve": "1;0.0000000;0.5000000;0.0000000;0.0000000;"
                + "0.1666667;0.3750000;0.0000000;0.0000000;"
                + "0.3333333;0.6250000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.6250000;0.0000000;0.0000000;"
                + "0.8333333;0.3750000;0.0000000;0.0000000;",
            },
        )
