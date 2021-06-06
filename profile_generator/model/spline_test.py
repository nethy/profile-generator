from typing import Callable
from unittest import TestCase

from .spline import fit, interpolate, solve


class SplineTest(TestCase):
    def test_solve_should_solve_nothing(self) -> None:
        self.assertEqual([], solve([], []))

    def test_solve_should_solve_linear_system(self) -> None:
        solution = solve([[3, 2, -4], [2, 3, 3], [5, -3, 1]], [3, 15, 14])
        for expected, actual in zip([3, 1, 2], solution):
            self.assertAlmostEqual(expected, actual)

    def test_interpolate_should_throw_error_at_no_point(self) -> None:
        spline = interpolate([])
        self.assertRaises(ValueError, spline, 0)

    def test_interpolate_should_interpolate_linear(self) -> None:
        spline = interpolate([(0, 0), (1, 1)])
        self.assertAlmostEqual(0.2, spline(0.2))
        self.assertAlmostEqual(0.7, spline(0.7))

    def test_interpolate_should_interpolate_non_linear(self) -> None:
        spline = interpolate(
            [
                (0, 21),
                (1, 24),
                (2, 24),
                (3, 18),
                (4, 16),
            ]
        )
        self.assertAlmostEqual(21, spline(0))
        self.assertAlmostEqual(22.6138393, spline(0.5))
        self.assertAlmostEqual(21.1272321, spline(2.5))
        self.assertAlmostEqual(16.4575893, spline(3.5))
        self.assertAlmostEqual(16, spline(4))

    def test_fit(self) -> None:
        self.assertEqual([(0, 1), (1, 1)], fit(lambda _: 1))
        self.assertEqual([(0, 0), (1, 1)], fit(lambda x: x))
        self.assertEqual(
            [
                (0, 0.0),
                (0.06666666666666667, 0.0044444444444444444),
                (0.16862745098039217, 0.028435217224144563),
                (0.5019607843137255, 0.2519646289888504),
                (0.8117647058823529, 0.658961937716263),
                (0.9254901960784314, 0.8565321030372934),
                (0.9725490196078431, 0.9458515955401768),
                (1, 1.0),
            ],
            fit(lambda x: x ** 2),
        )
        self._assert_fit(lambda x: x ** 2)

    def _assert_fit(self, fn: Callable[[float], float]) -> None:
        spline = interpolate(fit(fn))
        for x in (i / 255 for i in range(256)):
            self.assertAlmostEqual(spline(x), fn(x), 3)
