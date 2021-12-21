from unittest import TestCase

from .tone_curve import Point, algebraic_gamma, tone_curve_filmic

_GREY = Point(87 / 255, 119 / 255)


class TestToneCurve(TestCase):
    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_filmic(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.137182646)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.946651888)
        self.assertAlmostEqual(_curve(1), 1)

    def test_algebraic_gamma(self) -> None:
        _gamma = algebraic_gamma(1, 0.25, 0.5)

        self.assertAlmostEqual(_gamma(0), 0)
        self.assertAlmostEqual(_gamma(0.2), 0.4)
        self.assertAlmostEqual(_gamma(0.25), 0.5)
        self.assertAlmostEqual(_gamma(0.3), 0.5882353)
        self.assertAlmostEqual(_gamma(0.8), 0.9459459)
        self.assertAlmostEqual(_gamma(1), 1)
