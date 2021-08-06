from unittest import TestCase

from profile_generator.unit import Strength

from .sigmoid import (
    Point,
    contrast_of_gradient_exp,
    contrast_of_gradient_sqrt,
    gradient_of_contrast_exp,
    tone_curve_exp,
    tone_curve_hybrid,
    tone_curve_sqrt,
)

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_contrast_gradient(self) -> None:
        self.assertAlmostEqual(1, gradient_of_contrast_exp(0))
        self.assertAlmostEqual(1.8589818, gradient_of_contrast_exp(7))

    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_exp(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1479541)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9784533)
        self.assertAlmostEqual(_curve(1), 1)

    def test_tone_curve_sqrt(self) -> None:
        _curve = tone_curve_sqrt(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1551835)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9681931)
        self.assertAlmostEqual(_curve(1), 1)

    def test_find_contrast_gradient(self) -> None:
        slope = gradient_of_contrast_exp(8) / (235 / 255 - 16 / 255)
        self.assertAlmostEqual(9.4966168, contrast_of_gradient_exp(slope))

    def test_contrast_of_gradient_sqrt(self) -> None:
        self.assertAlmostEqual(12, contrast_of_gradient_sqrt(2))

    def test_tone_curve_hybrid_normal_hl_tone(self) -> None:
        _curve = tone_curve_hybrid(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1724979)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9566644)
        self.assertAlmostEqual(_curve(1), 1)

    def test_tone_curve_hybrid_max_tone_strength(self) -> None:
        _curve = tone_curve_hybrid(_GREY, 2, Strength(1))

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1479541)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9784533)
        self.assertAlmostEqual(_curve(1), 1)

    def test_tone_curve_hybrid_min_tone_strength(self) -> None:
        _curve = tone_curve_hybrid(_GREY, 2, Strength(-1))

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.2011133)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9353607)
        self.assertAlmostEqual(_curve(1), 1)
