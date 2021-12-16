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
                Point(x=0.111111, y=0.021026),
                Point(x=0.166667, y=0.053211),
                Point(x=0.222222, y=0.124736),
                Point(x=0.293651, y=0.307731),
                Point(x=0.388889, y=0.617179),
                Point(x=0.523810, y=0.857069),
                Point(x=0.626984, y=0.927326),
                Point(x=0.738095, y=0.964245),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.020696),
                Point(x=0.119048, y=0.052091),
                Point(x=0.158730, y=0.121551),
                Point(x=0.206349, y=0.285562),
                Point(x=0.253968, y=0.505280),
                Point(x=0.285714, y=0.638950),
                Point(x=0.396825, y=0.877545),
                Point(x=0.452381, y=0.919634),
                Point(x=0.515873, y=0.946903),
                Point(x=0.658730, y=0.976628),
                Point(x=1.000000, y=1.000000),
            ],
        )
