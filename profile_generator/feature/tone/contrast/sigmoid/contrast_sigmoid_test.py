from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)
_HL_PROTECTION = Strength(0.5)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.078431, y=0.025971),
                Point(x=0.211765, y=0.168923),
                Point(x=0.294118, y=0.347001),
                Point(x=0.396078, y=0.601549),
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
                Point(x=0.219608, y=0.194906),
                Point(x=0.298039, y=0.355266),
                Point(x=0.396078, y=0.596698),
                Point(x=0.541176, y=0.817895),
                Point(x=0.635294, y=0.874710),
                Point(x=0.749020, y=0.903906),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, offsets=_OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.078431, y=0.025971),
                Point(x=0.203922, y=0.155489),
                Point(x=0.298039, y=0.356759),
                Point(x=0.384314, y=0.572088),
                Point(x=0.517647, y=0.784105),
                Point(x=0.623529, y=0.861082),
                Point(x=0.737255, y=0.910929),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _STRENGTH, _HL_PROTECTION),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.211765, y=0.182904),
                Point(x=0.294118, y=0.345808),
                Point(x=0.388235, y=0.576017),
                Point(x=0.509804, y=0.753357),
                Point(x=0.615686, y=0.815984),
                Point(x=0.729412, y=0.853456),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _HL_PROTECTION, _OFFSETS),
        )
