from unittest import TestCase

from .sigmoid import algebraic, exponential


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

    def test_exponential(self) -> None:
        _curve = exponential(2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.0731484)
        self.assertAlmostEqual(_curve(0.5), 0.5)
        self.assertAlmostEqual(_curve(0.8), 0.9268516)
        self.assertAlmostEqual(_curve(1), 1)
