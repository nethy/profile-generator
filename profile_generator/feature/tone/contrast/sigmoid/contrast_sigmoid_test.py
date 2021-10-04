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
                Point(x=0.105882, y=0.012601),
                Point(x=0.211765, y=0.104100),
                Point(x=0.270588, y=0.241399),
                Point(x=0.333333, y=0.441545),
                Point(x=0.380392, y=0.578077),
                Point(x=0.529412, y=0.815587),
                Point(x=0.776471, y=0.959397),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.012126),
                Point(x=0.129412, y=0.093649),
                Point(x=0.168627, y=0.213520),
                Point(x=0.219608, y=0.426233),
                Point(x=0.258824, y=0.571494),
                Point(x=0.325490, y=0.726964),
                Point(x=0.400000, y=0.822888),
                Point(x=0.533333, y=0.915102),
                Point(x=0.662745, y=0.958541),
                Point(x=1.000000, y=1.000000),
            ],
        )
