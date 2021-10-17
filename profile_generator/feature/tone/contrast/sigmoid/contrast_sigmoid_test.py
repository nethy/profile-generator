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
                Point(x=0.103175, y=0.015115),
                Point(x=0.214286, y=0.117447),
                Point(x=0.269841, y=0.246261),
                Point(x=0.333333, y=0.441965),
                Point(x=0.388889, y=0.601159),
                Point(x=0.539683, y=0.848051),
                Point(x=0.666667, y=0.934579),
                Point(x=0.777778, y=0.970812),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.015811),
                Point(x=0.142857, y=0.109186),
                Point(x=0.182540, y=0.236423),
                Point(x=0.230159, y=0.439490),
                Point(x=0.269841, y=0.592458),
                Point(x=0.333333, y=0.754031),
                Point(x=0.404762, y=0.852793),
                Point(x=0.531746, y=0.934731),
                Point(x=0.666667, y=0.970919),
                Point(x=1.000000, y=1.000000),
            ],
        )
