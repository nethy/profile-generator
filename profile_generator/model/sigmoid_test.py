from unittest import TestCase

from .sigmoid import (
    Point,
    contrast_of_gamma_sqrt,
    contrast_of_gradient_exp,
    gamma_exp,
    gamma_gradient_exp,
    gamma_gradient_inverse_exp,
    gamma_gradient_inverse_sqrt,
    gamma_gradient_sqrt,
    gamma_inverse_exp,
    gamma_inverse_sqrt,
    gamma_of_exp,
    gamma_of_inverse_exp,
    gamma_of_inverse_sqrt,
    gamma_of_sqrt,
    gamma_sqrt,
    gradient_of_contrast_exp,
    tone_curve_exp,
    tone_curve_sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_gamma_sqrt(self) -> None:
        gamma = gamma_sqrt(2)
        inverse = gamma_inverse_sqrt(2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_sqrt(self) -> None:
        g = gamma_of_sqrt(_GREY.x, 0.5)
        gamma = gamma_sqrt(g)
        gamma_gradient = gamma_gradient_sqrt(g)

        self.assertAlmostEqual(0.5, gamma(_GREY.x))
        self.assertAlmostEqual(1.2439335, gamma_gradient(_GREY.x))

    def test_gamma_of_inverse_sqrt(self) -> None:
        g = gamma_of_inverse_sqrt(0.5, _GREY.y)
        gamma_inverse = gamma_inverse_sqrt(g)
        gamma_inverse_gradient = gamma_gradient_inverse_sqrt(g)

        self.assertAlmostEqual(_GREY.y, gamma_inverse(0.5))
        self.assertAlmostEqual(0.9734321, gamma_inverse_gradient(0.5))

    def test_gamma_exp(self) -> None:
        gamma = gamma_exp(2)
        inverse = gamma_inverse_exp(-2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_exp(self) -> None:
        g = gamma_of_exp(_GREY.x, 0.5)
        gamma = gamma_exp(g)
        gamma_gradient = gamma_gradient_exp(g)

        self.assertAlmostEqual(0.5, gamma(_GREY.x))
        self.assertAlmostEqual(1.1506553, gamma_gradient(_GREY.x))

    def test_gamma_of_inverse_exp(self) -> None:
        g = gamma_of_inverse_exp(0.5, _GREY.y)
        gamma_inverse = gamma_inverse_exp(g)
        gamma_inverse_gradient = gamma_gradient_inverse_exp(g)

        self.assertAlmostEqual(_GREY.y, gamma_inverse(0.5))
        self.assertAlmostEqual(0.9940811, gamma_inverse_gradient(0.5))

    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, gradient_of_contrast_exp(0))
        self.assertAlmostEqual(1.8589818, gradient_of_contrast_exp(7))

    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_exp(_GREY, 2)

        self.assertAlmostEqual(0.1959878, _curve(0.2))
        self.assertAlmostEqual(0.7377198, _curve(0.5))
        self.assertAlmostEqual(0.9563297, _curve(0.8))

    def test_tone_curve_sqrt(self) -> None:
        _curve = tone_curve_sqrt(_GREY, 2)

        self.assertAlmostEqual(0.1999008, _curve(0.2))
        self.assertAlmostEqual(0.7347897, _curve(0.5))
        self.assertAlmostEqual(0.9499429, _curve(0.8))

    def test_find_contrast_gradient(self) -> None:
        slope = gradient_of_contrast_exp(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.4966168, contrast_of_gradient_exp(slope))

    def test_contrast_of_gradient_sqrt(self) -> None:
        self.assertAlmostEqual(12, contrast_of_gamma_sqrt(2))
