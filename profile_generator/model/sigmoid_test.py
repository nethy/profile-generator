from unittest import TestCase

from .sigmoid import (
    Point,
    contrast_gradient,
    curve,
    find_contrast_gradient,
    gamma_gradient_reciprocal,
    gamma_inverse_gradient_reciprocal,
    gamma_inverse_reciprocal,
    gamma_of_inverse_reciprocal,
    gamma_of_reciprocal,
    gamma_reciprocal,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_gamma_reciprocal(self) -> None:
        gamma = gamma_reciprocal(2)
        inverse = gamma_inverse_reciprocal(2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_reciprocal(self) -> None:
        g = gamma_of_reciprocal(_GREY.x, 0.5)
        gamma = gamma_reciprocal(g)
        gamma_gradient = gamma_gradient_reciprocal(g)

        self.assertAlmostEqual(0.5, gamma(_GREY.x))
        self.assertAlmostEqual(1.1122229, gamma_gradient(_GREY.x))

    def test_gamma_of_inverse_reciprocal(self) -> None:
        g = gamma_of_inverse_reciprocal(0.5, _GREY.y)
        gamma_inverse = gamma_inverse_reciprocal(g)
        gamma_inverse_gradient = gamma_inverse_gradient_reciprocal(g)

        self.assertAlmostEqual(_GREY.y, gamma_inverse(0.5))
        self.assertAlmostEqual(0.9955556, gamma_inverse_gradient(0.5))

    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, contrast_gradient(0))
        self.assertAlmostEqual(1.8589818, contrast_gradient(7))

    def test_curve(self) -> None:
        _curve = curve(_GREY, 2)

        self.assertAlmostEqual(0.1912693, _curve(0.2))
        self.assertAlmostEqual(0.9582201, _curve(0.8))

    def test_curve_hl_protection(self) -> None:
        _curve = curve(_GREY, 2, 1.5)
        self.assertAlmostEqual(0.1912693, _curve(0.2))
        self.assertAlmostEqual(0.9229791, _curve(0.8))

    def test_find_contrast_slope(self) -> None:
        slope = contrast_gradient(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.4966168, find_contrast_gradient(slope))
