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
                Point(x=0.111111, y=0.016901),
                Point(x=0.214286, y=0.106306),
                Point(x=0.246032, y=0.169621),
                Point(x=0.285714, y=0.279637),
                Point(x=0.325397, y=0.412179),
                Point(x=0.349206, y=0.493119),
                Point(x=0.380952, y=0.585291),
                Point(x=0.436508, y=0.699710),
                Point(x=0.515873, y=0.802093),
                Point(x=0.634921, y=0.891377),
                Point(x=0.753968, y=0.942952),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.016595),
                Point(x=0.150794, y=0.098530),
                Point(x=0.198413, y=0.248556),
                Point(x=0.230159, y=0.392432),
                Point(x=0.253968, y=0.504405),
                Point(x=0.277778, y=0.597394),
                Point(x=0.333333, y=0.739622),
                Point(x=0.404762, y=0.838621),
                Point(x=0.531746, y=0.919217),
                Point(x=0.666667, y=0.958720),
                Point(x=1.000000, y=1.000000),
            ],
        )
