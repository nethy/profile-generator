import math
from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .matte import generate, get_matte_curve

DEFAULT = {"LCurve": "0;"}


class MatteTest(TestCase):
    def test_get_matte_curve_default(self) -> None:
        curve = get_matte_curve(0.0)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.25), 0.25)
        self.assertAlmostEqual(curve(0.5), 0.5)
        self.assertAlmostEqual(curve(0.75), 0.75)
        self.assertAlmostEqual(curve(1), 1)

    def test_get_matte_curve(self) -> None:
        curve = get_matte_curve(0.2)

        self.assertAlmostEqual(curve(0), 0.2)
        self.assertAlmostEqual(curve(0.1), 0.2146447)
        self.assertAlmostEqual(curve(0.5), 0.5)
        self.assertAlmostEqual(curve(0.9), 0.7592)
        self.assertAlmostEqual(curve(1), 0.8)

    def test_get_matte_curve_invalid(self) -> None:
        self.assertRaises(ValueError, get_matte_curve, -0.1)
        self.assertRaises(ValueError, get_matte_curve, 1 / (2 + math.sqrt(2)) + 1e-9)

    def test_generate_default(self) -> None:
        self.assertDictEqual(generate(ProfileParams(), False), DEFAULT)

    def test_generate(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.grading.matte.parse(5)

        self.assertDictEqual(
            generate(profile_params, False),
            {
                "LCurve": "4;0.0000000;0.1464466;0.0470588;0.1526442;"
                + "0.0941176;0.1617720;0.1411765;0.1767603;"
                + "0.1843137;0.1981505;0.2235294;0.2259052;"
                + "0.2588235;0.2588235;0.2941176;0.2941176;"
                + "0.3294118;0.3294118;0.3647059;0.3647059;"
                + "0.4000000;0.4000000;0.4352941;0.4352941;"
                + "0.4705882;0.4705882;0.5058824;0.5058521;"
                + "0.5411765;0.5397276;0.5764706;0.5715942;"
                + "0.6156863;0.6048336;0.6549020;0.6359956;"
                + "0.6941176;0.6652924;0.7333333;0.6929358;"
                + "0.7725490;0.7191378;0.8156863;0.7465482;"
                + "0.8588235;0.7727531;0.9019608;0.7980347;"
                + "0.9450980;0.8226751;0.9882353;0.8469564;"
                + "1.0000000;0.8535534;"
            },
        )
