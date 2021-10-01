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
                Point(x=0.098039, y=0.022019),
                Point(x=0.207843, y=0.126743),
                Point(x=0.301961, y=0.349743),
                Point(x=0.380392, y=0.576103),
                Point(x=0.450980, y=0.709195),
                Point(x=0.517647, y=0.788821),
                Point(x=0.752941, y=0.936791),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.125490, y=0.113588),
                Point(x=0.200000, y=0.352746),
                Point(x=0.262745, y=0.581494),
                Point(x=0.325490, y=0.716692),
                Point(x=0.392157, y=0.799587),
                Point(x=0.521569, y=0.891358),
                Point(x=0.658824, y=0.943303),
                Point(x=1.000000, y=1.000000),
            ],
        )
