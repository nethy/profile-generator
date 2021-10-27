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
                Point(x=0.095238, y=0.015916),
                Point(x=0.198413, y=0.109066),
                Point(x=0.380952, y=0.566972),
                Point(x=0.547619, y=0.831731),
                Point(x=0.769841, y=0.960837),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.063492, y=0.017548),
                Point(x=0.126984, y=0.103805),
                Point(x=0.166667, y=0.222332),
                Point(x=0.214286, y=0.404097),
                Point(x=0.261905, y=0.566870),
                Point(x=0.404762, y=0.822490),
                Point(x=0.539683, y=0.914070),
                Point(x=0.666667, y=0.957032),
                Point(x=1.000000, y=1.000000),
            ],
        )
