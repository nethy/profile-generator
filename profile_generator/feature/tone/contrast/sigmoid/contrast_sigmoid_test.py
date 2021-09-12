from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_GAMMA = 2.5
_EV_COMP = 1.0
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.121569, y=0.046534),
                Point(x=0.219608, y=0.152904),
                Point(x=0.294118, y=0.323090),
                Point(x=0.349020, y=0.490359),
                Point(x=0.384314, y=0.587524),
                Point(x=0.525490, y=0.819071),
                Point(x=0.627451, y=0.895043),
                Point(x=0.733333, y=0.941173),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_offests(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.121569, y=0.094098),
                Point(x=0.227451, y=0.185698),
                Point(x=0.298039, y=0.336529),
                Point(x=0.349020, y=0.490180),
                Point(x=0.384314, y=0.584423),
                Point(x=0.513725, y=0.777159),
                Point(x=0.619608, y=0.842110),
                Point(x=0.729412, y=0.878505),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_calculate_highlight_protection(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, highlight_protection=True),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.113725, y=0.041683),
                Point(x=0.215686, y=0.146433),
                Point(x=0.290196, y=0.311990),
                Point(x=0.349020, y=0.489997),
                Point(x=0.376471, y=0.561863),
                Point(x=0.435294, y=0.674994),
                Point(x=0.517647, y=0.778500),
                Point(x=0.745098, y=0.924881),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_ev_comp(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, ev_comp=_EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.078431, y=0.042959),
                Point(x=0.149020, y=0.150284),
                Point(x=0.200000, y=0.310425),
                Point(x=0.243137, y=0.488263),
                Point(x=0.274510, y=0.600874),
                Point(x=0.400000, y=0.835739),
                Point(x=0.529412, y=0.920331),
                Point(x=0.662745, y=0.959957),
                Point(x=1.000000, y=1.000000),
            ],
        )
