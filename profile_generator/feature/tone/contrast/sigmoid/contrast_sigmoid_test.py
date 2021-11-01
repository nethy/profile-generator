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
                Point(x=0.111111, y=0.022783),
                Point(x=0.214286, y=0.124870),
                Point(x=0.293651, y=0.315728),
                Point(x=0.373016, y=0.557026),
                Point(x=0.436508, y=0.685377),
                Point(x=0.523810, y=0.796468),
                Point(x=0.746032, y=0.935110),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.063492, y=0.018026),
                Point(x=0.134921, y=0.112452),
                Point(x=0.182540, y=0.261813),
                Point(x=0.214286, y=0.393707),
                Point(x=0.238095, y=0.494803),
                Point(x=0.261905, y=0.576262),
                Point(x=0.317460, y=0.702686),
                Point(x=0.388889, y=0.795755),
                Point(x=0.515873, y=0.883443),
                Point(x=0.650794, y=0.934862),
                Point(x=1.000000, y=1.000000),
            ],
        )
