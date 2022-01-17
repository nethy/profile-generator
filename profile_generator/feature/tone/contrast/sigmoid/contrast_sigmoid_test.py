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
                Point(x=0.103175, y=0.027079),
                Point(x=0.206349, y=0.132808),
                Point(x=0.380952, y=0.569175),
                Point(x=0.531746, y=0.818892),
                Point(x=0.634921, y=0.898384),
                Point(x=0.753968, y=0.949573),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.025172),
                Point(x=0.142857, y=0.119520),
                Point(x=0.285714, y=0.606188),
                Point(x=0.349206, y=0.763171),
                Point(x=0.412698, y=0.849661),
                Point(x=0.531746, y=0.925895),
                Point(x=0.674603, y=0.965397),
                Point(x=1.000000, y=1.000000),
            ],
        )
