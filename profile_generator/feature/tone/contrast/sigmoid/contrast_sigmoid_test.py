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
                Point(x=0.095238, y=0.017954),
                Point(x=0.206349, y=0.121807),
                Point(x=0.285714, y=0.303542),
                Point(x=0.373016, y=0.551521),
                Point(x=0.436508, y=0.679200),
                Point(x=0.523810, y=0.793094),
                Point(x=0.634921, y=0.879454),
                Point(x=0.753968, y=0.935308),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.020142),
                Point(x=0.134921, y=0.109121),
                Point(x=0.182540, y=0.260870),
                Point(x=0.238095, y=0.490725),
                Point(x=0.261905, y=0.572891),
                Point(x=0.317460, y=0.705511),
                Point(x=0.396825, y=0.812243),
                Point(x=0.523810, y=0.896767),
                Point(x=0.658730, y=0.943231),
                Point(x=1.000000, y=1.000000),
            ],
        )
