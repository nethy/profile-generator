from unittest import TestCase

from .matte import get_matte_curve


class MatteTest(TestCase):
    def test_get_matte_curve_default(self) -> None:
        self.assertIsNone(get_matte_curve(0.0))

    def test_get_matte_curve(self) -> None:
        curve = get_matte_curve(2.0)

        if curve is None:
            self.fail("curve cannot be None")
        self.assertAlmostEqual(curve(0), 0.0585786)
        self.assertAlmostEqual(curve(0.1), 0.1)
        self.assertAlmostEqual(curve(0.5), 0.5)
        self.assertAlmostEqual(curve(0.9), 0.8587606)
        self.assertAlmostEqual(curve(1), 0.9414214)

    def test_get_matte_curve_invalid(self) -> None:
        self.assertRaises(ValueError, get_matte_curve, -1e9)
        self.assertRaises(ValueError, get_matte_curve, 10.0 + 1e9)
