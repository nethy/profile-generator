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
                Point(x=0.111111, y=0.016967),
                Point(x=0.214286, y=0.108308),
                Point(x=0.285714, y=0.280872),
                Point(x=0.349206, y=0.493143),
                Point(x=0.380952, y=0.587263),
                Point(x=0.515873, y=0.818778),
                Point(x=0.626984, y=0.900646),
                Point(x=0.730159, y=0.943493),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.016657),
                Point(x=0.150794, y=0.100401),
                Point(x=0.206349, y=0.283563),
                Point(x=0.253968, y=0.504475),
                Point(x=0.277778, y=0.599970),
                Point(x=0.325397, y=0.736483),
                Point(x=0.396825, y=0.847161),
                Point(x=0.531746, y=0.929916),
                Point(x=0.658730, y=0.963172),
                Point(x=1.000000, y=1.000000),
            ],
        )
