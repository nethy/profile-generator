from unittest import TestCase

from .sigmoid import (
    Point,
    contrast_of_gamma_sqrt,
    contrast_of_gradient_exp,
    gradient_of_contrast_exp,
    tone_curve_exp,
    tone_curve_sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, gradient_of_contrast_exp(0))
        self.assertAlmostEqual(1.8589818, gradient_of_contrast_exp(7))

    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_exp(_GREY, 2)

        self.assertAlmostEqual(_curve(0.2), 0.1851187)
        self.assertAlmostEqual(_curve(0.5), 0.7484923)
        self.assertAlmostEqual(_curve(0.8), 0.9614034)

    def test_tone_curve_sqrt(self) -> None:
        _curve = tone_curve_sqrt(_GREY, 2)

        self.assertAlmostEqual(_curve(0.2), 0.1829012)
        self.assertAlmostEqual(_curve(0.5), 0.7543625)
        self.assertAlmostEqual(_curve(0.8), 0.9576714)

    def test_find_contrast_gradient(self) -> None:
        slope = gradient_of_contrast_exp(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.4966168, contrast_of_gradient_exp(slope))

    def test_contrast_of_gradient_sqrt(self) -> None:
        self.assertAlmostEqual(12, contrast_of_gamma_sqrt(2))
