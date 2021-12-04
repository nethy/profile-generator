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
                Point(x=0.126984, y=0.037680),
                Point(x=0.182540, y=0.079927),
                Point(x=0.230159, y=0.146001),
                Point(x=0.293651, y=0.304830),
                Point(x=0.341270, y=0.466646),
                Point(x=0.380952, y=0.588643),
                Point(x=0.436508, y=0.714183),
                Point(x=0.523810, y=0.835826),
                Point(x=0.626984, y=0.911958),
                Point(x=0.730159, y=0.952986),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.087302, y=0.034662),
                Point(x=0.126984, y=0.073759),
                Point(x=0.158730, y=0.129407),
                Point(x=0.206349, y=0.282824),
                Point(x=0.253968, y=0.504713),
                Point(x=0.285714, y=0.629434),
                Point(x=0.404762, y=0.865438),
                Point(x=0.468254, y=0.912647),
                Point(x=0.531746, y=0.940374),
                Point(x=0.666667, y=0.971727),
                Point(x=1.000000, y=1.000000),
            ],
        )
