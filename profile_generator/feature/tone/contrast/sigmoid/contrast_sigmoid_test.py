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
                Point(x=0.103175, y=0.031888),
                Point(x=0.206349, y=0.142742),
                Point(x=0.388889, y=0.585140),
                Point(x=0.539683, y=0.830456),
                Point(x=0.642857, y=0.907883),
                Point(x=0.761905, y=0.955954),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.036005),
                Point(x=0.142857, y=0.129423),
                Point(x=0.285714, y=0.603276),
                Point(x=0.349206, y=0.764311),
                Point(x=0.412698, y=0.853994),
                Point(x=0.531746, y=0.930686),
                Point(x=0.674603, y=0.968518),
                Point(x=1.000000, y=1.000000),
            ],
        )
