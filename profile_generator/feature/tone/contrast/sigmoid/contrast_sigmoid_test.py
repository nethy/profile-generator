from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY = Point(87 / 255, 119 / 255)
_GAMMA = 2.5
_GAIN = (2.0, 2.0)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.027292),
                Point(x=0.215686, y=0.186001),
                Point(x=0.294118, y=0.349854),
                Point(x=0.396078, y=0.597715),
                Point(x=0.545098, y=0.832633),
                Point(x=0.639216, y=0.904599),
                Point(x=0.749020, y=0.951909),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.121569, y=0.108421),
                Point(x=0.223529, y=0.211081),
                Point(x=0.298039, y=0.357336),
                Point(x=0.400000, y=0.601744),
                Point(x=0.533333, y=0.792684),
                Point(x=0.631373, y=0.853564),
                Point(x=0.741176, y=0.888302),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_gain(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.117647, y=0.034859),
                Point(x=0.211765, y=0.139487),
                Point(x=0.262745, y=0.250227),
                Point(x=0.321569, y=0.414811),
                Point(x=0.356863, y=0.506502),
                Point(x=0.392157, y=0.597200),
                Point(x=0.462745, y=0.751718),
                Point(x=0.549020, y=0.869267),
                Point(x=0.749020, y=0.973433),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA, _GAIN),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.117647, y=0.085753),
                Point(x=0.223529, y=0.180643),
                Point(x=0.270588, y=0.274787),
                Point(x=0.325490, y=0.422546),
                Point(x=0.356863, y=0.503351),
                Point(x=0.400000, y=0.611400),
                Point(x=0.454902, y=0.721577),
                Point(x=0.533333, y=0.817020),
                Point(x=0.627451, y=0.873089),
                Point(x=0.741176, y=0.903018),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, _GAIN, _OFFSETS),
        )
