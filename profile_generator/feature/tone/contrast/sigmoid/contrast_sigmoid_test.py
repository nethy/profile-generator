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
                Point(x=0.119048, y=0.021661),
                Point(x=0.174603, y=0.054490),
                Point(x=0.222222, y=0.115098),
                Point(x=0.277778, y=0.250776),
                Point(x=0.341270, y=0.466646),
                Point(x=0.380952, y=0.588129),
                Point(x=0.436508, y=0.708739),
                Point(x=0.515873, y=0.814052),
                Point(x=0.634921, y=0.901371),
                Point(x=0.753968, y=0.949603),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.018535),
                Point(x=0.119048, y=0.046924),
                Point(x=0.158730, y=0.112025),
                Point(x=0.198413, y=0.243954),
                Point(x=0.246032, y=0.468091),
                Point(x=0.277778, y=0.600816),
                Point(x=0.325397, y=0.733983),
                Point(x=0.396825, y=0.842377),
                Point(x=0.460317, y=0.893098),
                Point(x=0.523810, y=0.924555),
                Point(x=0.658730, y=0.962386),
                Point(x=1.000000, y=1.000000),
            ],
        )
