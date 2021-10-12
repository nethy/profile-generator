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
                Point(x=0.105882, y=0.016043),
                Point(x=0.211765, y=0.113024),
                Point(x=0.274510, y=0.259555),
                Point(x=0.333333, y=0.441965),
                Point(x=0.384314, y=0.589476),
                Point(x=0.537255, y=0.845649),
                Point(x=0.768627, y=0.968656),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.070588, y=0.015387),
                Point(x=0.141176, y=0.105148),
                Point(x=0.176471, y=0.213263),
                Point(x=0.231373, y=0.444664),
                Point(x=0.270588, y=0.594951),
                Point(x=0.403922, y=0.851944),
                Point(x=0.541176, y=0.938361),
                Point(x=0.666667, y=0.970919),
                Point(x=1.000000, y=1.000000),
            ],
        )
