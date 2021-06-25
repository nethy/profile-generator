from unittest import TestCase

from .linalg import inverse, solve


class LinalgTest(TestCase):
    def test_solve_should_solve_nothing(self) -> None:
        self.assertEqual([], solve([]))

    def test_solve_should_solve_linear_system(self) -> None:
        solution = solve([[3, 2, -4, 3], [2, 3, 3, 15], [5, -3, 1, 14]])
        for expected, actual in zip([3, 1, 2], solution):
            self.assertAlmostEqual(expected, float(actual))

    def test_inverse_matrix(self) -> None:
        expected = [
            [-11 / 12, 1 / 3, 1 / 12],
            [-1 / 6, 1 / 3, -1 / 6],
            [3 / 4, -1 / 3, 1 / 12],
        ]
        result = inverse([[1, 2, 3], [4, 5, 6], [7, 2, 9]])
        for expected_row, row in zip(expected, result):
            for a, b in zip(expected_row, row):
                self.assertAlmostEqual(a, b)
