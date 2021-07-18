from unittest import TestCase

from profile_generator.unit import Point

from .gamma import (
    gamma_exp,
    gamma_gradient_exp,
    gamma_gradient_inverse_exp,
    gamma_gradient_inverse_linear,
    gamma_gradient_inverse_sqrt,
    gamma_gradient_linear,
    gamma_gradient_sqrt,
    gamma_inverse_exp,
    gamma_inverse_linear,
    gamma_inverse_sqrt,
    gamma_linear,
    gamma_of_exp,
    gamma_of_inverse_exp,
    gamma_of_inverse_linear,
    gamma_of_inverse_sqrt,
    gamma_of_linear,
    gamma_of_sqrt,
    gamma_sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class GammaTest(TestCase):
    def test_gamma_linear(self) -> None:
        gamma = gamma_linear(2)
        inverse = gamma_inverse_linear(2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_linear(self) -> None:
        g = gamma_of_linear(_GREY.x, 0.5)
        gamma = gamma_linear(g)
        gamma_gradient = gamma_gradient_linear(g)

        self.assertAlmostEqual(g, 0.9310345)
        self.assertAlmostEqual(0.5, gamma(_GREY.x))
        self.assertAlmostEqual(1.1122229, gamma_gradient(_GREY.x))

    def test_gamma_of_inverse_linear(self) -> None:
        g = gamma_of_inverse_linear(0.5, _GREY.y)
        gamma_inverse = gamma_inverse_linear(g)
        gamma_inverse_gradient = gamma_gradient_inverse_linear(g)

        self.assertAlmostEqual(_GREY.y, gamma_inverse(0.5))
        self.assertAlmostEqual(0.9955556, gamma_inverse_gradient(0.5))

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

        self.assertAlmostEqual(g, 1.3650177)
        self.assertAlmostEqual(0.5, gamma(_GREY.x))
        self.assertAlmostEqual(1.1506553, gamma_gradient(_GREY.x))

    def test_gamma_of_inverse_exp(self) -> None:
        g = gamma_of_inverse_exp(0.5, _GREY.y)
        gamma_inverse = gamma_inverse_exp(g)
        gamma_inverse_gradient = gamma_gradient_inverse_exp(g)

        self.assertAlmostEqual(_GREY.y, gamma_inverse(0.5))
        self.assertAlmostEqual(0.9940811, gamma_inverse_gradient(0.5))
