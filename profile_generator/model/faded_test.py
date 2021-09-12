from unittest import TestCase

from .faded import curve


class FadedTest(TestCase):
    def test_curve(self) -> None:
        _curve = curve(0.2, 0.1)

        self.assertAlmostEqual(_curve(0), 0.2)
        self.assertAlmostEqual(_curve(0.3333333), 0.3333333)
        self.assertAlmostEqual(_curve(1), 1)
