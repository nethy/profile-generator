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
                Point(x=0.111111, y=0.018764),
                Point(x=0.214286, y=0.107284),
                Point(x=0.253968, y=0.191314),
                Point(x=0.293651, y=0.307310),
                Point(x=0.380952, y=0.589926),
                Point(x=0.436508, y=0.714746),
                Point(x=0.515873, y=0.823276),
                Point(x=0.619048, y=0.900544),
                Point(x=0.730159, y=0.946813),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.018458),
                Point(x=0.119048, y=0.048424),
                Point(x=0.158730, y=0.117978),
                Point(x=0.206349, y=0.284925),
                Point(x=0.238095, y=0.430511),
                Point(x=0.253968, y=0.504972),
                Point(x=0.277778, y=0.602937),
                Point(x=0.325397, y=0.741028),
                Point(x=0.396825, y=0.851593),
                Point(x=0.460317, y=0.900949),
                Point(x=0.531746, y=0.933590),
                Point(x=0.658730, y=0.965738),
                Point(x=1.000000, y=1.000000),
            ],
        )
