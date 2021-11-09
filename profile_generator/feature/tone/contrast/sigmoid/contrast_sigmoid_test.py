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
                Point(x=0.103175, y=0.021092),
                Point(x=0.214286, y=0.123604),
                Point(x=0.293651, y=0.310731),
                Point(x=0.325397, y=0.412778),
                Point(x=0.349206, y=0.492942),
                Point(x=0.380952, y=0.583937),
                Point(x=0.436508, y=0.701083),
                Point(x=0.523810, y=0.815474),
                Point(x=0.642857, y=0.900299),
                Point(x=0.769841, y=0.950527),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.019521),
                Point(x=0.150794, y=0.115774),
                Point(x=0.206349, y=0.289676),
                Point(x=0.230159, y=0.393588),
                Point(x=0.253968, y=0.504078),
                Point(x=0.277778, y=0.596040),
                Point(x=0.325397, y=0.726345),
                Point(x=0.404762, y=0.844355),
                Point(x=0.523810, y=0.919747),
                Point(x=0.666667, y=0.960568),
                Point(x=1.000000, y=1.000000),
            ],
        )
