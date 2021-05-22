from unittest import TestCase

from .sigmoid import (
    Point,
    brightness_gradient,
    contrast_gradient,
    curve,
    curve_with_hl_protection,
    find_contrast_gradient,
    find_curve_brightness,
)

_GREY = Point(87 / 255, 119 / 255)

_PLACES = 5


class SigmoidTest(TestCase):
    def test_find_curve_brightness(self) -> None:
        self.assertAlmostEqual(1.19759, find_curve_brightness(_GREY, 7), _PLACES)
        self.assertAlmostEqual(1.19779, find_curve_brightness(_GREY, -7), _PLACES)

    def test_brightness_gradient(self) -> None:
        self.assertAlmostEqual(1, brightness_gradient(0)(0.3), _PLACES)
        self.assertAlmostEqual(0.85092, brightness_gradient(2)(0.5), _PLACES)

    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, contrast_gradient(0), _PLACES)
        self.assertAlmostEqual(1.85898, contrast_gradient(7), _PLACES)

    def test_curve(self) -> None:
        _curve = curve(1, 7)

        self.assertAlmostEqual(0.17658, _curve(0.2), _PLACES)
        self.assertAlmostEqual(0.95109, _curve(0.8), _PLACES)

    def test_curve_with_hl_protection(self) -> None:
        _curve = curve_with_hl_protection(1, 7)

        self.assertAlmostEqual(0.17658, _curve(0.2), _PLACES)
        self.assertAlmostEqual(0.90762, _curve(0.8), _PLACES)

    def test_find_contrast_slope(self) -> None:
        slope = contrast_gradient(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.49662, find_contrast_gradient(slope), _PLACES)
