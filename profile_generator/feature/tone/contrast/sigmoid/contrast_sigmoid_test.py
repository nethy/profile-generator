from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_SLOPE = 2.5
_BRIGHTNESS = 1.0


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.111111, y=0.024448),
                Point(x=0.214286, y=0.125858),
                Point(x=0.293651, y=0.320502),
                Point(x=0.380952, y=0.580234),
                Point(x=0.444444, y=0.713092),
                Point(x=0.523810, y=0.816439),
                Point(x=0.642857, y=0.902782),
                Point(x=0.753968, y=0.948059),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.024062),
                Point(x=0.150794, y=0.117497),
                Point(x=0.198413, y=0.268216),
                Point(x=0.238095, y=0.433608),
                Point(x=0.261905, y=0.533795),
                Point(x=0.285714, y=0.618854),
                Point(x=0.325397, y=0.725293),
                Point(x=0.404762, y=0.845918),
                Point(x=0.531746, y=0.925539),
                Point(x=0.666667, y=0.962755),
                Point(x=1.000000, y=1.000000),
            ],
        )
