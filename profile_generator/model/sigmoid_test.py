from unittest import TestCase

from .sigmoid import _gradient_of_inverse_contrast_exp, exp


class SigmoidTest(TestCase):
    def test_gradient_of_inverse_contrast_exp(self) -> None:
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0), 1)
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0.95), 0.5186210)
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0.99), 0.3740574)

    def test_contrast_curve_exp_negative(self) -> None:
        _curve = exp(0.5)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.32918671)
        self.assertAlmostEqual(_curve(0.5), 0.5)
        self.assertAlmostEqual(_curve(0.8), 0.67081329)
        self.assertAlmostEqual(_curve(1), 1)
