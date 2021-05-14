from unittest import TestCase

from .sigmoid import (
    Point,
    contrast_slope,
    curve,
    curve_with_hl_protection,
    find_contrast_slope,
    find_curve_brightness,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_find_curve_brightness(self) -> None:
        self.assertEqual(1.2109756469726562, find_curve_brightness(_GREY, 7))
        self.assertEqual(0.8556365966796875, find_curve_brightness(_GREY, -7))

    def test_contrast_slope(self) -> None:
        self.assertEqual(1.8589818074022992, contrast_slope(7))

    def test_curve(self) -> None:
        self.assertEqual(0.1638150623355538, curve(7, 1, 0.2))
        self.assertEqual(0.9575595972571656, curve(7, 1, 0.8))

    def test_curve_with_hl_protection(self) -> None:
        self.assertEqual(0.1638150623355538, curve_with_hl_protection(7, 1, 0.2))
        self.assertEqual(0.9225177590875977, curve_with_hl_protection(7, 1, 0.8))

    def test_find_contrast_slope(self) -> None:
        slope = contrast_slope(8) / (235 / 255 - 16 / 255)
        self.assertEqual(9.496593475341797, find_contrast_slope(slope))
