from unittest import TestCase

from .sigmoid import (
    Point,
    brightness_gradient,
    contrast_gradient,
    curve,
    find_contrast_gradient,
    find_curve_brightness,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_find_curve_brightness(self) -> None:
        self.assertAlmostEqual(1.1975829, find_curve_brightness(_GREY, 7))
        self.assertAlmostEqual(1.1977866, find_curve_brightness(_GREY, -7))

    def test_brightness_gradient(self) -> None:
        self.assertAlmostEqual(1, brightness_gradient(0)(0.3))
        self.assertAlmostEqual(0.8509181, brightness_gradient(2)(0.5))

    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, contrast_gradient(0))
        self.assertAlmostEqual(1.8589818, contrast_gradient(7))

    def test_curve(self) -> None:
        _curve = curve(1, 7)

        self.assertAlmostEqual(0.1765795, _curve(0.2))
        self.assertAlmostEqual(0.9510898, _curve(0.8))

    def test_curve_hl_protection(self) -> None:
        _curve = curve(1, 7, 4)
        self.assertAlmostEqual(0.1765795, _curve(0.2))
        self.assertAlmostEqual(0.8995560, _curve(0.8))

    def test_find_contrast_slope(self) -> None:
        slope = contrast_gradient(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.4966168, find_contrast_gradient(slope))
