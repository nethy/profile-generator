from unittest import TestCase

from .sigmoid import Point, approximate_brightness, contrast_slope

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_approximate_brightness(self) -> None:
        self.assertEqual(1.2109756469726562, approximate_brightness(_GREY, 7))
        self.assertEqual(0.8556365966796875, approximate_brightness(_GREY, -7))

    def test_contrast_slope(self) -> None:
        self.assertEqual(1.8589818074022992, contrast_slope(7))
