from unittest import TestCase

from .sigmoid import (
    Point,
    brightness_slope,
    contrast_gradient,
    find_contrast_gradient,
    find_curve_brightness,
    get_curve,
    get_curve_with_hl_protection,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_find_curve_brightness(self) -> None:
        self.assertEqual(1.197582483291626, find_curve_brightness(_GREY, 7))
        self.assertEqual(0.8597612380981445, find_curve_brightness(_GREY, -7))

    def test_brightness_slope(self) -> None:
        self.assertEqual(0.5, brightness_slope(0)(0.5))
        self.assertEqual(0.8509181282393214, brightness_slope(2)(0.5))

    def test_contrast_slope(self) -> None:
        self.assertEqual(1, contrast_gradient(0))
        self.assertEqual(1.8589818074022992, contrast_gradient(7))

    def test_curve(self) -> None:
        curve = get_curve(7, 1)

        self.assertEqual(0.1638150623355538, curve(0.2))
        self.assertEqual(0.9575595972571656, curve(0.8))

    def test_curve_with_hl_protection(self) -> None:
        curve = get_curve_with_hl_protection(7, 1)

        self.assertEqual(0.1638150623355538, curve(0.2))
        self.assertEqual(0.912111374617178, curve(0.8))

    def test_find_contrast_slope(self) -> None:
        slope = contrast_gradient(8) / (235 / 255 - 16 / 255)
        self.assertEqual(9.496617317199707, find_contrast_gradient(slope))
