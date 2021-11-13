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
                Point(x=0.111111, y=0.017782),
                Point(x=0.222222, y=0.124981),
                Point(x=0.293651, y=0.306668),
                Point(x=0.349206, y=0.493383),
                Point(x=0.388889, y=0.613257),
                Point(x=0.531746, y=0.857314),
                Point(x=0.642857, y=0.932918),
                Point(x=0.761905, y=0.971118),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.017455),
                Point(x=0.158730, y=0.121764),
                Point(x=0.206349, y=0.284576),
                Point(x=0.253968, y=0.504951),
                Point(x=0.285714, y=0.634094),
                Point(x=0.404762, y=0.878847),
                Point(x=0.531746, y=0.951152),
                Point(x=0.666667, y=0.978634),
                Point(x=1.000000, y=1.000000),
            ],
        )
