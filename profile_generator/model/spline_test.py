from typing import Callable
from unittest import TestCase

from .spline import fit, interpolate, inverse_matrix, solve


class SplineTest(TestCase):
    def test_solve_should_solve_nothing(self) -> None:
        self.assertEqual([], solve([]))

    def test_solve_should_solve_linear_system(self) -> None:
        solution = solve([[3, 2, -4, 3], [2, 3, 3, 15], [5, -3, 1, 14]])
        for expected, actual in zip([3, 1, 2], solution):
            self.assertAlmostEqual(expected, float(actual))

    def test_interpolate_should_be_zero_when_no_points(self) -> None:
        spline = interpolate([])
        self.assertEqual(0.0, spline(0.0))
        self.assertEqual(0.0, spline(1.0))
        self.assertEqual(0.0, spline(10.0))

    def test_interpolate_should_be_constant_when_single_point(self) -> None:
        spline = interpolate([(0.0, 0.5)])
        self.assertEqual(0.5, spline(0.0))
        self.assertEqual(0.5, spline(1.0))

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
        self._assert_fit(lambda x: x ** 16)

    def test_inverse_matrix(self) -> None:
        expected = [
            [-11 / 12, 1 / 3, 1 / 12],
            [-1 / 6, 1 / 3, -1 / 6],
            [3 / 4, -1 / 3, 1 / 12],
        ]
        inverse = inverse_matrix([[1, 2, 3], [4, 5, 6], [7, 2, 9]])
        for expected_row, row in zip(expected, inverse):
            for a, b in zip(expected_row, row):
                self.assertAlmostEqual(a, b)

    def _assert_fit(self, fn: Callable[[float], float]) -> None:
        spline = interpolate(fit(fn))
        for x in (i / 255 for i in range(256)):
            self.assertAlmostEqual(spline(x), fn(x), 2)
