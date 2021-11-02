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
                Point(x=0.103175, y=0.021390),
                Point(x=0.206349, y=0.121937),
                Point(x=0.277778, y=0.283018),
                Point(x=0.349206, y=0.489067),
                Point(x=0.380952, y=0.570326),
                Point(x=0.531746, y=0.811424),
                Point(x=0.761905, y=0.947714),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.023752),
                Point(x=0.134921, y=0.115736),
                Point(x=0.182540, y=0.265128),
                Point(x=0.238095, y=0.484523),
                Point(x=0.261905, y=0.565116),
                Point(x=0.317460, y=0.700762),
                Point(x=0.396825, y=0.811979),
                Point(x=0.523810, y=0.899248),
                Point(x=0.658730, y=0.946041),
                Point(x=1.000000, y=1.000000),
            ],
        )
