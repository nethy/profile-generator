from unittest import TestCase

from .limited import curve


class LimitedTest(TestCase):
    def test_curve(self) -> None:
        _curve = curve(0.25, 0.8)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.25), 0.25)
        self.assertAlmostEqual(_curve(0.5), 0.4703704)
        self.assertAlmostEqual(_curve(1), 0.8)
