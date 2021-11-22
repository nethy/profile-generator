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
                Point(x=0.119048, y=0.028342),
                Point(x=0.222222, y=0.137251),
                Point(x=0.301587, y=0.335199),
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
                Point(x=0.087302, y=0.029480),
                Point(x=0.158730, y=0.134104),
                Point(x=0.214286, y=0.322814),
                Point(x=0.253968, y=0.504475),
                Point(x=0.285714, y=0.627443),
                Point(x=0.396825, y=0.847161),
                Point(x=0.523810, y=0.926962),
                Point(x=0.658730, y=0.963172),
                Point(x=1.000000, y=1.000000),
            ],
        )
