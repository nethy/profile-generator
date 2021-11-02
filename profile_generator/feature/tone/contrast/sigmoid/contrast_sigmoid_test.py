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
                Point(x=0.103175, y=0.021390),
                Point(x=0.206349, y=0.121937),
                Point(x=0.277778, y=0.283018),
                Point(x=0.373016, y=0.549941),
                Point(x=0.436508, y=0.676287),
                Point(x=0.531746, y=0.798666),
                Point(x=0.761905, y=0.938365),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.020249),
                Point(x=0.134921, y=0.106649),
                Point(x=0.182540, y=0.256794),
                Point(x=0.238095, y=0.485320),
                Point(x=0.261905, y=0.567508),
                Point(x=0.317460, y=0.700434),
                Point(x=0.388889, y=0.799016),
                Point(x=0.515873, y=0.888145),
                Point(x=0.658730, y=0.939911),
                Point(x=1.000000, y=1.000000),
            ],
        )
