from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY = Point(87 / 255, 119 / 255)
_GAMMA = 2.5
_HL_PROTECTION = 2.5
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.082353, y=0.027076),
                Point(x=0.207843, y=0.162525),
                Point(x=0.286275, y=0.328911),
                Point(x=0.396078, y=0.599328),
                Point(x=0.552941, y=0.853619),
                Point(x=0.654902, y=0.928806),
                Point(x=0.772549, y=0.970894),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.215686, y=0.188800),
                Point(x=0.294118, y=0.346605),
                Point(x=0.396078, y=0.594883),
                Point(x=0.545098, y=0.817498),
                Point(x=0.639216, y=0.873564),
                Point(x=0.752941, y=0.903166),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.078431, y=0.025030),
                Point(x=0.196078, y=0.142906),
                Point(x=0.290196, y=0.338481),
                Point(x=0.372549, y=0.541737),
                Point(x=0.498039, y=0.742227),
                Point(x=0.611765, y=0.820896),
                Point(x=0.741176, y=0.874187),
                Point(x=0.898039, y=0.943932),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA, _HL_PROTECTION),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.207843, y=0.177049),
                Point(x=0.290196, y=0.337271),
                Point(x=0.380392, y=0.555261),
                Point(x=0.498039, y=0.726663),
                Point(x=0.607843, y=0.789019),
                Point(x=0.729412, y=0.827931),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, _HL_PROTECTION, _OFFSETS),
        )
