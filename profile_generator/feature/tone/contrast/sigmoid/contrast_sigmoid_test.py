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
                Point(x=0.125490, y=0.049103),
                Point(x=0.227451, y=0.166559),
                Point(x=0.298039, y=0.334378),
                Point(x=0.400000, y=0.637506),
                Point(x=0.529412, y=0.857396),
                Point(x=0.631373, y=0.927858),
                Point(x=0.737255, y=0.963935),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_offests(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.125490, y=0.095897),
                Point(x=0.231373, y=0.191662),
                Point(x=0.301961, y=0.347560),
                Point(x=0.396078, y=0.624075),
                Point(x=0.513725, y=0.809615),
                Point(x=0.619608, y=0.869725),
                Point(x=0.729412, y=0.896954),
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
                Point(x=0.243137, y=0.488565),
                Point(x=0.282353, y=0.637306),
                Point(x=0.400000, y=0.870367),
                Point(x=0.529412, y=0.947047),
                Point(x=0.666667, y=0.976655),
                Point(x=1.000000, y=1.000000),
            ],
        )
