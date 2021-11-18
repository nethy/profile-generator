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
                Point(x=0.349206, y=0.492738),
                Point(x=0.373016, y=0.560562),
                Point(x=0.436508, y=0.688812),
                Point(x=0.515873, y=0.788642),
                Point(x=0.626984, y=0.874038),
                Point(x=0.746032, y=0.930968),
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
                Point(x=0.253968, y=0.503670),
                Point(x=0.277778, y=0.591605),
                Point(x=0.325397, y=0.712136),
                Point(x=0.404762, y=0.824922),
                Point(x=0.523810, y=0.904560),
                Point(x=0.666667, y=0.951657),
                Point(x=1.000000, y=1.000000),
            ],
        )
