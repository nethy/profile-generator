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
                Point(x=0.103175, y=0.022262),
                Point(x=0.206349, y=0.123176),
                Point(x=0.261905, y=0.243353),
                Point(x=0.325397, y=0.422294),
                Point(x=0.373016, y=0.547133),
                Point(x=0.539683, y=0.816060),
                Point(x=0.769841, y=0.952188),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.021444),
                Point(x=0.134921, y=0.103128),
                Point(x=0.174603, y=0.217813),
                Point(x=0.230159, y=0.439744),
                Point(x=0.261905, y=0.552864),
                Point(x=0.396825, y=0.806782),
                Point(x=0.523810, y=0.896399),
                Point(x=0.658730, y=0.944903),
                Point(x=1.000000, y=1.000000),
            ],
        )
