from unittest import TestCase

from .tone_curve import Point, flat_gamma, tone_curve_filmic

_GREY = Point(87 / 255, 119 / 255)


class TestToneCurve(TestCase):
    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_filmic(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.14479477)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.947612761)
        self.assertAlmostEqual(_curve(1), 1)

    def test_flat_gamma(self) -> None:
        _gamma = flat_gamma(0.25, 0.5)

        self.assertAlmostEqual(_gamma(0), 0)
        self.assertAlmostEqual(_gamma(0.1), 0.2)
        self.assertAlmostEqual(_gamma(0.25), 0.5)
        self.assertAlmostEqual(_gamma(0.6), 0.8620690)
        self.assertAlmostEqual(_gamma(0.9), 0.9756098)
        self.assertAlmostEqual(_gamma(1), 1)
