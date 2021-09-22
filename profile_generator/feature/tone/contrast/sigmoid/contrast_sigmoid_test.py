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
                Point(x=0.098039, y=0.019012),
                Point(x=0.207843, y=0.120272),
                Point(x=0.286275, y=0.299108),
                Point(x=0.372549, y=0.552518),
                Point(x=0.435294, y=0.674994),
                Point(x=0.517647, y=0.778500),
                Point(x=0.745098, y=0.924881),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.070588, y=0.019010),
                Point(x=0.149020, y=0.118829),
                Point(x=0.203922, y=0.290425),
                Point(x=0.231373, y=0.404379),
                Point(x=0.250980, y=0.488671),
                Point(x=0.274510, y=0.572875),
                Point(x=0.329412, y=0.707728),
                Point(x=0.403922, y=0.814718),
                Point(x=0.525490, y=0.894924),
                Point(x=0.666667, y=0.939931),
                Point(x=1.000000, y=1.000000),
            ],
        )
