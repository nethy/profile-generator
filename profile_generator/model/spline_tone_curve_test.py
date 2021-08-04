from unittest import TestCase

from .spline_tone_curve import Point, curve


class SplineToneCurveTest(TestCase):
    def test_curve(self) -> None:
        _curve = curve(Point(87 / 255, 119 / 255), 2.2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(87 / 255), 119 / 255)
        self.assertAlmostEqual(_curve(1), 1)
        self.assertAlmostEqual(_curve(0.8), 0.9643288)
        self.assertAlmostEqual(_curve(0.2), 0.1960280)
