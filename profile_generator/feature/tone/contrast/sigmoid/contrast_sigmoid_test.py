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
                Point(x=0.119048, y=0.032175),
                Point(x=0.174603, y=0.072584),
                Point(x=0.222222, y=0.135558),
                Point(x=0.293651, y=0.307858),
                Point(x=0.325397, y=0.412282),
                Point(x=0.349206, y=0.492766),
                Point(x=0.380952, y=0.584067),
                Point(x=0.436508, y=0.701957),
                Point(x=0.523810, y=0.816301),
                Point(x=0.650794, y=0.905466),
                Point(x=0.769841, y=0.951771),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.087302, y=0.033317),
                Point(x=0.158730, y=0.132562),
                Point(x=0.206349, y=0.286362),
                Point(x=0.230159, y=0.392722),
                Point(x=0.253968, y=0.503857),
                Point(x=0.277778, y=0.596274),
                Point(x=0.396825, y=0.833298),
                Point(x=0.452381, y=0.877604),
                Point(x=0.523810, y=0.914318),
                Point(x=0.658730, y=0.954914),
                Point(x=1.000000, y=1.000000),
            ],
        )
