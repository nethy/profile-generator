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
                Point(x=0.214286, y=0.159427),
                Point(x=0.285714, y=0.315289),
                Point(x=0.388889, y=0.590568),
                Point(x=0.539683, y=0.836495),
                Point(x=0.634921, y=0.906565),
                Point(x=0.746032, y=0.952163),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.150794, y=0.151248),
                Point(x=0.206349, y=0.317540),
                Point(x=0.246032, y=0.467745),
                Point(x=0.293651, y=0.634309),
                Point(x=0.349206, y=0.771913),
                Point(x=0.412698, y=0.859197),
                Point(x=0.531746, y=0.932587),
                Point(x=0.674603, y=0.969003),
                Point(x=1.000000, y=1.000000),
            ],
        )
