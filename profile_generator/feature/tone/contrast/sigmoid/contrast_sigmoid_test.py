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
                Point(x=0.095238, y=0.016125),
                Point(x=0.206349, y=0.119875),
                Point(x=0.261905, y=0.243345),
                Point(x=0.333333, y=0.444503),
                Point(x=0.380952, y=0.569239),
                Point(x=0.539683, y=0.825584),
                Point(x=0.650794, y=0.910938),
                Point(x=0.761905, y=0.958465),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.063492, y=0.015886),
                Point(x=0.126984, y=0.092289),
                Point(x=0.166667, y=0.206327),
                Point(x=0.222222, y=0.423596),
                Point(x=0.261905, y=0.564330),
                Point(x=0.404762, y=0.825106),
                Point(x=0.539683, y=0.914610),
                Point(x=0.666667, y=0.957038),
                Point(x=1.000000, y=1.000000),
            ],
        )
