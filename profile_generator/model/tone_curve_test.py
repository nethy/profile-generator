from unittest import TestCase

from .tone_curve import Point, filmic

_GREY = Point(87 / 255, 119 / 255)


class TestToneCurve(TestCase):
    def test_filmic(self) -> None:
        _curve = filmic(_GREY, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.130953249)
        self.assertAlmostEqual(_curve(_GREY.x), _GREY.y)
        self.assertAlmostEqual(_curve(0.8), 0.947980155)
        self.assertAlmostEqual(_curve(1), 1)
