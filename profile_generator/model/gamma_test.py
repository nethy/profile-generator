from unittest import TestCase

from profile_generator.unit import Point

from .gamma import (
    _exp,
    _inverse_exp,
    _inverse_linear,
    _inverse_sqrt,
    _linear,
    _sqrt,
    exp,
    inverse_exp,
    inverse_linear,
    inverse_sqrt,
    linear,
    sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class GammaTest(TestCase):
    def test_gamma_linear(self) -> None:
        gamma = _linear(2)
        inverse = _inverse_linear(2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_linear(self) -> None:
        gamma, gradient = linear(_GREY.x, 0.5)

        self.assertAlmostEqual(gamma(_GREY.x), 0.5)
        self.assertAlmostEqual(gradient, 1.1122229)

    def test_gamma_of_inverse_linear(self) -> None:
        gamma_inverse, gradient = inverse_linear(0.5, _GREY.y)

        self.assertAlmostEqual(gamma_inverse(0.5), _GREY.y)
        self.assertAlmostEqual(gradient, 0.9955556)

    def test_gamma_sqrt(self) -> None:
        gamma = _sqrt(2)
        inverse = _inverse_sqrt(2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_sqrt(self) -> None:
        gamma, gradient = sqrt(_GREY.x, 0.5)

        self.assertAlmostEqual(gamma(_GREY.x), 0.5)
        self.assertAlmostEqual(gradient, 1.2439335)

    def test_gamma_of_inverse_sqrt(self) -> None:
        gamma_inverse, gradient = inverse_sqrt(0.5, _GREY.y)

        self.assertAlmostEqual(gamma_inverse(0.5), _GREY.y)
        self.assertAlmostEqual(gradient, 0.9734321)

    def test_gamma_exp(self) -> None:
        gamma = _exp(2)
        inverse = _inverse_exp(-2)

        self.assertAlmostEqual(0, inverse(gamma(0)))
        self.assertAlmostEqual(0.5, inverse(gamma(0.5)))
        self.assertAlmostEqual(1, inverse(gamma(1)))

    def test_gamma_of_exp(self) -> None:
        gamma, gradient = exp(_GREY.x, 0.5)

        self.assertAlmostEqual(gamma(_GREY.x), 0.5)
        self.assertAlmostEqual(gradient, 1.2668930)

    def test_gamma_of_inverse_exp(self) -> None:
        gamma_inverse, gradient = inverse_exp(0.5, _GREY.y)

        self.assertAlmostEqual(gamma_inverse(0.5), _GREY.y)
        self.assertAlmostEqual(gradient, 0.9725837)
