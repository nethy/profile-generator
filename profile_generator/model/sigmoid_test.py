from unittest import TestCase

from .sigmoid import Point, tone_curve_exp, tone_curve_sqrt

_GREY = Point(87 / 255, 119 / 255)


class SigmoidTest(TestCase):
    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_exp(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1496112)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9816715)
        self.assertAlmostEqual(_curve(1), 1)

    def test_tone_curve_sqrt(self) -> None:
        _curve = tone_curve_sqrt(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1595593)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9682817)
        self.assertAlmostEqual(_curve(1), 1)
