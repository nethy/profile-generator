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
                Point(x=0.111111, y=0.021262),
                Point(x=0.166667, y=0.054360),
                Point(x=0.214286, y=0.114500),
                Point(x=0.309524, y=0.361315),
                Point(x=0.333333, y=0.439669),
                Point(x=0.357143, y=0.519516),
                Point(x=0.388889, y=0.613244),
                Point(x=0.507937, y=0.813273),
                Point(x=0.619048, y=0.896563),
                Point(x=0.722222, y=0.941061),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.020925),
                Point(x=0.150794, y=0.106425),
                Point(x=0.174603, y=0.171336),
                Point(x=0.222222, y=0.358446),
                Point(x=0.238095, y=0.430703),
                Point(x=0.261905, y=0.540458),
                Point(x=0.285714, y=0.633607),
                Point(x=0.333333, y=0.759276),
                Point(x=0.396825, y=0.848379),
                Point(x=0.523810, y=0.927106),
                Point(x=0.658730, y=0.963467),
                Point(x=1.000000, y=1.000000),
            ],
        )
