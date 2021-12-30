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
                Point(x=0.087302, y=0.016658),
                Point(x=0.190476, y=0.105249),
                Point(x=0.293651, y=0.343029),
                Point(x=0.365079, y=0.522832),
                Point(x=0.539683, y=0.798229),
                Point(x=0.753968, y=0.934194),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.063492, y=0.016972),
                Point(x=0.134921, y=0.100413),
                Point(x=0.166667, y=0.184910),
                Point(x=0.222222, y=0.382670),
                Point(x=0.277778, y=0.568373),
                Point(x=0.349206, y=0.735458),
                Point(x=0.420635, y=0.829747),
                Point(x=0.539683, y=0.909481),
                Point(x=0.674603, y=0.953976),
                Point(x=1.000000, y=1.000000),
            ],
        )
