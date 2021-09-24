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
                Point(x=0.211765, y=0.126845),
                Point(x=0.286275, y=0.299108),
                Point(x=0.349020, y=0.490233),
                Point(x=0.380392, y=0.575409),
                Point(x=0.435294, y=0.690389),
                Point(x=0.525490, y=0.810789),
                Point(x=0.639216, y=0.893728),
                Point(x=0.756863, y=0.942592),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.129412, y=0.116303),
                Point(x=0.184314, y=0.287288),
                Point(x=0.235294, y=0.488869),
                Point(x=0.258824, y=0.569017),
                Point(x=0.313725, y=0.703388),
                Point(x=0.392157, y=0.813459),
                Point(x=0.521569, y=0.899130),
                Point(x=0.658824, y=0.943564),
                Point(x=1.000000, y=1.000000),
            ],
        )
