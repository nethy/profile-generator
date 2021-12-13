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
                Point(x=0.111111, y=0.016573),
                Point(x=0.166667, y=0.043767),
                Point(x=0.214286, y=0.097832),
                Point(x=0.246032, y=0.162352),
                Point(x=0.277778, y=0.252106),
                Point(x=0.380952, y=0.588871),
                Point(x=0.452381, y=0.731811),
                Point(x=0.515873, y=0.807046),
                Point(x=0.658730, y=0.907254),
                Point(x=0.777778, y=0.953095),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.016306),
                Point(x=0.119048, y=0.042784),
                Point(x=0.158730, y=0.108287),
                Point(x=0.198413, y=0.245174),
                Point(x=0.253968, y=0.504790),
                Point(x=0.277778, y=0.601628),
                Point(x=0.333333, y=0.746514),
                Point(x=0.396825, y=0.834907),
                Point(x=0.523810, y=0.919128),
                Point(x=0.658730, y=0.959242),
                Point(x=1.000000, y=1.000000),
            ],
        )
