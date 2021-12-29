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
                Point(x=0.119048, y=0.028127),
                Point(x=0.174603, y=0.066129),
                Point(x=0.214286, y=0.116299),
                Point(x=0.246032, y=0.182580),
                Point(x=0.285714, y=0.299970),
                Point(x=0.325397, y=0.418996),
                Point(x=0.365079, y=0.531620),
                Point(x=0.428571, y=0.659282),
                Point(x=0.515873, y=0.771561),
                Point(x=0.753968, y=0.926009),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.024219),
                Point(x=0.150794, y=0.108797),
                Point(x=0.174603, y=0.173931),
                Point(x=0.206349, y=0.303131),
                Point(x=0.230159, y=0.402379),
                Point(x=0.269841, y=0.555427),
                Point(x=0.325397, y=0.695141),
                Point(x=0.404762, y=0.808580),
                Point(x=0.531746, y=0.897020),
                Point(x=0.666667, y=0.945124),
                Point(x=1.000000, y=1.000000),
            ],
        )
