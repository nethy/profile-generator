from unittest import TestCase

from .tone_curve import Point, tone_curve_filmic

_GREY = Point(87 / 255, 119 / 255)


class TestToneCurve(TestCase):
    def test_tone_curve_exp(self) -> None:
        _curve = tone_curve_filmic(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1513090)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.9355453)
        self.assertAlmostEqual(_curve(1), 1)
