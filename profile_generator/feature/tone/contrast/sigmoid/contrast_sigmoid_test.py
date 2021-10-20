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
                Point(x=0.103175, y=0.012363),
                Point(x=0.214286, y=0.108891),
                Point(x=0.261905, y=0.218972),
                Point(x=0.325397, y=0.416521),
                Point(x=0.380952, y=0.581020),
                Point(x=0.539683, y=0.850118),
                Point(x=0.658730, y=0.934641),
                Point(x=0.777778, y=0.974389),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.013303),
                Point(x=0.134921, y=0.086779),
                Point(x=0.166667, y=0.180186),
                Point(x=0.222222, y=0.418228),
                Point(x=0.261905, y=0.575613),
                Point(x=0.333333, y=0.755633),
                Point(x=0.396825, y=0.841729),
                Point(x=0.531746, y=0.930798),
                Point(x=0.658730, y=0.968013),
                Point(x=1.000000, y=1.000000),
            ],
        )
