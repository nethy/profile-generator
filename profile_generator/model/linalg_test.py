from unittest import TestCase

from .linalg import Matrix, Vector, inverse, multiply_vector_vector, scale_matrix, solve


class LinalgTestCase(TestCase):
    def assert_vector_equal(self, left: Vector, right: Vector, places: int = 7) -> None:
        self.assertEqual(
            len(left), len(right), "length incorrect: left is {0}, but right is {1}"
        )
        for a, b in zip(left, right):
            diff = abs(a - b)
            if round(diff, places) != 0:
                message = (
                    f"{[round(x, places) for x in left]} != "
                    + f"{[round(x, places) for x in right]}"
                )
                raise self.failureException(message)

    def assert_matrix_equal(self, left: Matrix, right: Matrix, places: int = 7) -> None:
        if len(left) == 0 and len(right) == 0:
            return

        self.assertEqual(
            len(left), len(right), "length incorrect: left is {0}, but right is {1}"
        )
        self.assertEqual(
            len(left[0]),
            len(right[0]),
            "length incorrect: left is {0}, but right is {1}",
        )
        for left_row, right_row in zip(left, right):
            for a, b in zip(left_row, right_row):
                diff = abs(a - b)
                if round(diff, places) != 0:
                    message = (
                        f"{[[round(x, places) for x in row] for row in left]} != "
                        + f"{[[round(x, places) for x in row] for row in right]}"
                    )
                    raise self.failureException(message)


class LinalgTest(LinalgTestCase):
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
        self.assert_matrix_equal(result, expected)

    def test_multiply_vector_vector(self) -> None:
        self.assertEqual(multiply_vector_vector([1, 2, 3], [4, 5, 6]), 4 + 10 + 18)

    def test_scale_matrix(self) -> None:
        self.assert_matrix_equal(
            scale_matrix([1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            [[1, 2, 3], [8, 10, 12], [21, 24, 27]],
        )
