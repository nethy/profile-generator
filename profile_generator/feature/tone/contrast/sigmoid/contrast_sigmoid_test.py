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
                Point(x=0.111111, y=0.024448),
                Point(x=0.206349, y=0.112437),
                Point(x=0.246032, y=0.191541),
                Point(x=0.285714, y=0.297195),
                Point(x=0.325397, y=0.417240),
                Point(x=0.349206, y=0.490490),
                Point(x=0.373016, y=0.555237),
                Point(x=0.436508, y=0.686959),
                Point(x=0.523810, y=0.801135),
                Point(x=0.634921, y=0.886083),
                Point(x=0.753968, y=0.940126),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.024062),
                Point(x=0.150794, y=0.117497),
                Point(x=0.198413, y=0.268216),
                Point(x=0.230159, y=0.399460),
                Point(x=0.253968, y=0.500647),
                Point(x=0.277778, y=0.586173),
                Point(x=0.349206, y=0.757043),
                Point(x=0.396825, y=0.818661),
                Point(x=0.523810, y=0.904510),
                Point(x=0.658730, y=0.949101),
                Point(x=1.000000, y=1.000000),
            ],
        )
