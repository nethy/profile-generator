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
                Point(x=0.105882, y=0.013271),
                Point(x=0.211765, y=0.106565),
                Point(x=0.270588, y=0.243879),
                Point(x=0.333333, y=0.441872),
                Point(x=0.380392, y=0.576715),
                Point(x=0.529412, y=0.813325),
                Point(x=0.772549, y=0.957244),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.012776),
                Point(x=0.129412, y=0.096016),
                Point(x=0.164706, y=0.201642),
                Point(x=0.215686, y=0.410551),
                Point(x=0.258824, y=0.570202),
                Point(x=0.325490, y=0.724657),
                Point(x=0.400000, y=0.820648),
                Point(x=0.533333, y=0.913490),
                Point(x=0.662745, y=0.957573),
                Point(x=1.000000, y=1.000000),
            ],
        )
