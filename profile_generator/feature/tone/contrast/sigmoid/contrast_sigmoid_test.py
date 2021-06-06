from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate, calculate_with_hl_protection

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.027451, y=0.006338),
                Point(x=0.078431, y=0.025971),
                Point(x=0.149020, y=0.080501),
                Point(x=0.211765, y=0.168923),
                Point(x=0.294118, y=0.347001),
                Point(x=0.396078, y=0.601549),
                Point(x=0.470588, y=0.750330),
                Point(x=0.552941, y=0.859028),
                Point(x=0.647059, y=0.928981),
                Point(x=0.756863, y=0.969503),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _STRENGTH),
        )

    def test_calculate_linear(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(1.00000, 1.00000),
            ],
            calculate(Point(0.5, 0.5), Strength()),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.105882, y=0.087241),
                Point(x=0.219608, y=0.194906),
                Point(x=0.298039, y=0.355266),
                Point(x=0.349020, y=0.483393),
                Point(x=0.396078, y=0.596698),
                Point(x=0.466667, y=0.730263),
                Point(x=0.541176, y=0.817895),
                Point(x=0.635294, y=0.874710),
                Point(x=0.749020, y=0.903906),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.027451, y=0.006338),
                Point(x=0.074510, y=0.023995),
                Point(x=0.196078, y=0.142747),
                Point(x=0.286275, y=0.327713),
                Point(x=0.325490, y=0.426459),
                Point(x=0.360784, y=0.513930),
                Point(x=0.384314, y=0.561949),
                Point(x=0.407843, y=0.605869),
                Point(x=0.454902, y=0.680954),
                Point(x=0.525490, y=0.765551),
                Point(x=0.623529, y=0.845540),
                Point(x=0.737255, y=0.909023),
                Point(x=0.886275, y=0.967424),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.105882, y=0.087241),
                Point(x=0.207843, y=0.177197),
                Point(x=0.286275, y=0.327226),
                Point(x=0.325490, y=0.423664),
                Point(x=0.341176, y=0.463530),
                Point(x=0.349020, y=0.483393),
                Point(x=0.368627, y=0.525502),
                Point(x=0.415686, y=0.610817),
                Point(x=0.521569, y=0.737826),
                Point(x=0.623529, y=0.806590),
                Point(x=0.737255, y=0.855887),
                Point(x=0.913725, y=0.905013),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
