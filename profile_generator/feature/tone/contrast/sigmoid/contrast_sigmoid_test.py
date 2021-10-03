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
                Point(x=0.117647, y=0.016918),
                Point(x=0.223529, y=0.104066),
                Point(x=0.274510, y=0.224611),
                Point(x=0.301961, y=0.321108),
                Point(x=0.329412, y=0.426533),
                Point(x=0.372549, y=0.556353),
                Point(x=0.517647, y=0.788821),
                Point(x=0.741176, y=0.932197),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.074510, y=0.018631),
                Point(x=0.141176, y=0.102055),
                Point(x=0.176471, y=0.215244),
                Point(x=0.200000, y=0.325133),
                Point(x=0.219608, y=0.423471),
                Point(x=0.254902, y=0.557532),
                Point(x=0.317647, y=0.703923),
                Point(x=0.392157, y=0.799587),
                Point(x=0.529412, y=0.895235),
                Point(x=0.654902, y=0.942189),
                Point(x=1.000000, y=1.000000),
            ],
        )
