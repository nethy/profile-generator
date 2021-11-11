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
                Point(x=0.111111, y=0.025395),
                Point(x=0.214286, y=0.130903),
                Point(x=0.293651, y=0.320138),
                Point(x=0.349206, y=0.490778),
                Point(x=0.380952, y=0.575902),
                Point(x=0.436508, y=0.688881),
                Point(x=0.523810, y=0.802954),
                Point(x=0.642857, y=0.890197),
                Point(x=0.753968, y=0.938170),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.020654),
                Point(x=0.142857, y=0.111523),
                Point(x=0.198413, y=0.285368),
                Point(x=0.246032, y=0.487103),
                Point(x=0.269841, y=0.574667),
                Point(x=0.317460, y=0.700422),
                Point(x=0.396825, y=0.818413),
                Point(x=0.523810, y=0.902030),
                Point(x=0.658730, y=0.944979),
                Point(x=1.000000, y=1.000000),
            ],
        )
