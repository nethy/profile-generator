from unittest import TestCase

from .sigmoid import algebraic, mask


class SigmoidTest(TestCase):
    def test_algebraic_linear(self) -> None:
        _curve = algebraic(2, 1)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.125)
        self.assertAlmostEqual(_curve(0.5), 0.5)
        self.assertAlmostEqual(_curve(0.8), 0.875)
        self.assertAlmostEqual(_curve(1), 1)

    def test_algebraic_cubic(self) -> None:
        _curve = algebraic(2, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.0839749)
        self.assertAlmostEqual(_curve(0.5), 0.5)
        self.assertAlmostEqual(_curve(0.8), 0.9160251)
        self.assertAlmostEqual(_curve(1), 1)

    def test_mask(self) -> None:
        curve = mask(0.2, 0.6)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.2), 0)
        self.assertAlmostEqual(curve(0.3), 0.13166491925514737)
        self.assertAlmostEqual(curve(0.4), 0.5)
        self.assertAlmostEqual(curve(0.5), 0.8683350807448527)
        self.assertAlmostEqual(curve(0.6), 1)
        self.assertAlmostEqual(curve(1), 1)
