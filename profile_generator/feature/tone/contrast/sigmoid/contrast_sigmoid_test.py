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
                Point(x=0.105882, y=0.031163),
                Point(x=0.215686, y=0.144024),
                Point(x=0.286275, y=0.302005),
                Point(x=0.341176, y=0.466327),
                Point(x=0.384314, y=0.581072),
                Point(x=0.443137, y=0.704305),
                Point(x=0.525490, y=0.814121),
                Point(x=0.615686, y=0.884307),
                Point(x=0.729412, y=0.938449),
                Point(x=0.878431, y=0.981399),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.078431, y=0.032793),
                Point(x=0.152941, y=0.138540),
                Point(x=0.207843, y=0.308591),
                Point(x=0.247059, y=0.471755),
                Point(x=0.282353, y=0.599935),
                Point(x=0.341176, y=0.752454),
                Point(x=0.392157, y=0.818287),
                Point(x=0.517647, y=0.896605),
                Point(x=0.658824, y=0.939627),
                Point(x=0.894118, y=0.986122),
                Point(x=1.000000, y=1.000000),
            ],
        )
