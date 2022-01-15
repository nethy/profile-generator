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
                Point(x=0.111111, y=0.035502),
                Point(x=0.206349, y=0.137986),
                Point(x=0.388889, y=0.589907),
                Point(x=0.452381, y=0.722738),
                Point(x=0.539683, y=0.840271),
                Point(x=0.634921, y=0.911225),
                Point(x=0.746032, y=0.955952),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.034980),
                Point(x=0.150794, y=0.143273),
                Point(x=0.293651, y=0.633958),
                Point(x=0.349206, y=0.774140),
                Point(x=0.412698, y=0.863418),
                Point(x=0.531746, y=0.936976),
                Point(x=0.674603, y=0.971899),
                Point(x=1.000000, y=1.000000),
            ],
        )
