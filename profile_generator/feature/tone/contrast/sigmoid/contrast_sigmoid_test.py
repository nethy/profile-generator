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
                Point(x=0.117647, y=0.028293),
                Point(x=0.215686, y=0.130815),
                Point(x=0.286275, y=0.295742),
                Point(x=0.384314, y=0.591336),
                Point(x=0.509804, y=0.803754),
                Point(x=0.611765, y=0.881439),
                Point(x=0.721569, y=0.933301),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.133333, y=0.123076),
                Point(x=0.180392, y=0.268729),
                Point(x=0.223529, y=0.442547),
                Point(x=0.262745, y=0.586889),
                Point(x=0.384314, y=0.814180),
                Point(x=0.517647, y=0.902627),
                Point(x=0.650980, y=0.948360),
                Point(x=1.000000, y=1.000000),
            ],
        )
