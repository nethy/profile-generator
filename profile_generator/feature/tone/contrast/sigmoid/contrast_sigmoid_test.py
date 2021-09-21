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
                Point(x=0.113725, y=0.035484),
                Point(x=0.219608, y=0.150795),
                Point(x=0.290196, y=0.312885),
                Point(x=0.341176, y=0.466327),
                Point(x=0.388235, y=0.596612),
                Point(x=0.447059, y=0.724554),
                Point(x=0.529412, y=0.836807),
                Point(x=0.627451, y=0.908999),
                Point(x=0.737255, y=0.953192),
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
                Point(x=0.247059, y=0.471957),
                Point(x=0.290196, y=0.633014),
                Point(x=0.341176, y=0.768451),
                Point(x=0.396078, y=0.844508),
                Point(x=0.521569, y=0.921696),
                Point(x=0.662745, y=0.958439),
                Point(x=1.000000, y=1.000000),
            ],
        )
