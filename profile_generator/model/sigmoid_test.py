from unittest import TestCase

from .sigmoid import (
    Point,
    _gradient_of_inverse_contrast_exp,
    contrast_curve_exp,
    tone_curve_exp,
    tone_curve_sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_exp(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1515006)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9772645)
        self.assertAlmostEqual(_curve(1), 1)

    def test_tone_curve_sqrt(self) -> None:
        _curve = tone_curve_sqrt(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1590238)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.96897062)
        self.assertAlmostEqual(_curve(1), 1)

    def test_gradient_of_inverse_contrast_exp(self) -> None:
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0), 1)
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0.95), 0.5186210)
        self.assertAlmostEqual(_gradient_of_inverse_contrast_exp(0.99), 0.3740574)

    def test_contrast_curve_exp_negative(self) -> None:
        _curve = contrast_curve_exp(0.5)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.32918671)
        self.assertAlmostEqual(_curve(0.5), 0.5)
        self.assertAlmostEqual(_curve(0.8), 0.67081329)
        self.assertAlmostEqual(_curve(1), 1)
