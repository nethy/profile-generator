from unittest import TestCase

from profile_generator.unit import Point

from .gamma import algebraic_at, log_at

_GREY = Point(87 / 255, 119 / 255)


class GammaTest(TestCase):
    def test_algebraic_at_linear(self) -> None:
        gamma = algebraic_at(Point(0.25, 0.5), 1)

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.25), 0.5)
        self.assertAlmostEqual(gamma(0.5), 0.75)
        self.assertAlmostEqual(gamma(1), 1)

    def test_algebraic_at_cubic(self) -> None:
        gamma = algebraic_at(Point(0.25, 0.5), 2)

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.25), 0.5)
        self.assertAlmostEqual(gamma(0.5), 0.7905694)
        self.assertAlmostEqual(gamma(1), 1)

    def test_algebraic_at_inverse_linear(self) -> None:
        gamma = algebraic_at(Point(0.5, 0.25), 1)

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.5), 0.25)
        self.assertAlmostEqual(gamma(0.75), 0.5)
        self.assertAlmostEqual(gamma(1), 1)

    def test_algebraic_at_inverse_cubic(self) -> None:
        gamma = algebraic_at(Point(0.5, 0.25), 2)

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.5), 0.25)
        self.assertAlmostEqual(gamma(0.7905694), 0.5)
        self.assertAlmostEqual(gamma(1), 1)

    def test_log_at(self) -> None:
        gamma = log_at(Point(0.25, 0.5))

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.25), 0.5)
        self.assertAlmostEqual(gamma(0.5), 0.7324868)
        self.assertAlmostEqual(gamma(1), 1)

    def test_log_at_inverse(self) -> None:
        gamma = log_at(Point(0.5, 0.25))

        self.assertAlmostEqual(gamma(0), 0)
        self.assertAlmostEqual(gamma(0.5), 0.25)
        self.assertAlmostEqual(gamma(0.732486760), 0.5)
        self.assertAlmostEqual(gamma(1), 1)
