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
                Point(x=0.349206, y=0.493010),
                Point(x=0.380952, y=0.585170),
                Point(x=0.436508, y=0.705178),
                Point(x=0.523810, y=0.821851),
                Point(x=0.642857, y=0.906014),
                Point(x=0.769841, y=0.954110),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.087302, y=0.029480),
                Point(x=0.158730, y=0.134104),
                Point(x=0.206349, y=0.289676),
                Point(x=0.230159, y=0.393588),
                Point(x=0.253968, y=0.504214),
                Point(x=0.285714, y=0.624211),
                Point(x=0.404762, y=0.850842),
                Point(x=0.531746, y=0.927852),
                Point(x=0.666667, y=0.963541),
                Point(x=1.000000, y=1.000000),
            ],
        )
