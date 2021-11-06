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
                Point(x=0.111111, y=0.027132),
                Point(x=0.206349, y=0.123241),
                Point(x=0.277778, y=0.282118),
                Point(x=0.373016, y=0.550005),
                Point(x=0.444444, y=0.689288),
                Point(x=0.539683, y=0.812456),
                Point(x=0.769841, y=0.951098),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.024094),
                Point(x=0.134921, y=0.108377),
                Point(x=0.190476, y=0.277204),
                Point(x=0.238095, y=0.468747),
                Point(x=0.261905, y=0.552727),
                Point(x=0.309524, y=0.675072),
                Point(x=0.396825, y=0.803490),
                Point(x=0.515873, y=0.887570),
                Point(x=0.658730, y=0.942049),
                Point(x=1.000000, y=1.000000),
            ],
        )
