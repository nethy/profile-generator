from unittest import TestCase

from .sigmoid import Point, approximate_brightness


class SigmoidTest(TestCase):
    def test_approximate_brightness(self) -> None:
        grey = Point(87 / 255, 119 / 255)
        contrast = 7

        self.assertEqual(1.2109756469726562, approximate_brightness(grey, contrast))
