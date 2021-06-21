import bisect
import math
from collections.abc import Callable, Sequence

Matrix = list[list[float]]
Vector = list[float]
Point = tuple[float, float]

EPSILON = 1 / 256 / 2


def fit(fn: Callable[[float], float]) -> Sequence[Point]:
    references = [(i / 255, fn(i / 255)) for i in range(1, 255)]
    knots = [(0.0, fn(0.0)), (1.0, fn(1.0))]
    for _ in range(3, 24 + 1):
        spline = interpolate(knots)
        max_diff, i = _find_max_diff(references, spline)
        if max_diff > EPSILON:
            knot = references.pop(i)
            bisect.insort(knots, knot)
        else:
            break
    return knots


def _find_max_diff(
    references: list[Point], spline: Callable[[float], float]
) -> tuple[float, int]:
    return max(((abs(y - spline(x)), i) for i, (x, y) in enumerate(references)))


def interpolate(points: Sequence[Point]) -> Callable[[float], float]:
    if len(points) == 0:
        return lambda x: 0.0
    elif len(points) == 1:
        return lambda x: points[0][1]
    xs, ys = [x for x, _ in points], [y for _, y in points]
    system = _equations(xs, ys)
    coefficients = solve(system)
    return lambda x: _spline(x, xs, coefficients)


def _equations(xs: Vector, ys: Vector) -> Matrix:
    n = len(xs)
    system = [[0.0 for _ in range((n - 1) * 4 + 1)] for _ in range((n - 1) * 4)]
    _fn_equations(system, xs, ys)
    _dx_equations(system, xs)
    _second_dx_equations(system, xs)
    _boundaries(system, xs)
    return system


def _fn_equations(matrix: Matrix, xs: Vector, ys: Vector) -> None:
    n = len(xs)
    for i in range(n - 1):
        x, y = xs[i], ys[i]
        matrix[i * 2][i * 4 : (i + 1) * 4] = [x ** 3, x ** 2, x, 1.0]
        matrix[i * 2][-1] = y
        x, y = xs[i + 1], ys[i + 1]
        matrix[i * 2 + 1][i * 4 : (i + 1) * 4] = [x ** 3, x ** 2, x, 1.0]
        matrix[i * 2 + 1][-1] = y


def _dx_equations(matrix: Matrix, xs: Vector) -> None:
    n = len(xs)
    for i in range(n - 2):
        x = xs[i + 1]
        offset = 2 * (n - 1)
        matrix[offset + i][i * 4 : (i + 2) * 4] = [
            3 * x ** 2,
            2 * x,
            1.0,
            0.0,
            -3 * x ** 2,
            -2 * x,
            -1.0,
            0.0,
        ]


def _second_dx_equations(coefficients: Matrix, xs: Vector) -> None:
    n = len(xs)
    for i in range(n - 2):
        x = xs[i + 1]
        offset = 3 * (n - 1) - 1
        coefficients[offset + i][i * 4 : (i + 2) * 4] = [
            6 * x,
            2.0,
            0.0,
            0.0,
            -6 * x,
            -2.0,
            0.0,
            0.0,
        ]


def _boundaries(coefficients: Matrix, xs: Vector) -> None:
    n = len(xs)
    x = xs[0]
    coefficients[-2][:2] = [6 * x, 2.0]
    x = xs[-1]
    coefficients[-1][(n - 2) * 4 : (n - 2) * 4 + 2] = [6 * x, 2.0]


def _spline(x: float, knots: Vector, coefficients: Vector) -> float:
    y = 0.0
    for i in range(len(knots) - 1):
        if knots[i] <= x <= knots[i + 1]:
            a, b, c, d = coefficients[i * 4 : i * 4 + 4]
            y = a * x ** 3 + b * x ** 2 + c * x + d
            break
    return y


def solve(system: Matrix) -> Vector:
    _inverse(system)
    return [line[-1] for line in system]


def inverse_matrix(matrix: Matrix) -> Matrix:
    unit_matrix = [[0.0] * len(matrix) for _ in range(len(matrix))]
    for i, row in enumerate(unit_matrix):
        row[i] = 1.0
    system = [row + unit_row for row, unit_row in zip(matrix, unit_matrix)]
    _inverse(system)
    return [row[len(system) :] for row in system]


def _inverse(matrix: Matrix) -> None:
    pivot_idx = 0
    for row in range(len(matrix)):
        if not pivot_idx < len(matrix[0]):
            break
        pivot_idx = _swap_row(matrix, row, pivot_idx)
        if pivot_idx < len(matrix[0]):
            _normalize(matrix, row, pivot_idx)
            _eliminate_column(matrix, row, pivot_idx)
            pivot_idx += 1


def _swap_row(matrix: Matrix, row: int, pivot_idx: int) -> int:
    i = row
    while pivot_idx < len(matrix[0]) and math.isclose(matrix[i][pivot_idx], 0):
        i += 1
        if i == len(matrix):
            i = row
            pivot_idx += 1

    if i < len(matrix):
        matrix[row], matrix[i] = matrix[i], matrix[row]

    return pivot_idx


def _normalize(matrix: Matrix, row: int, pivot_idx: int) -> None:
    divisor = matrix[row][pivot_idx]
    matrix[row] = [value / divisor for value in matrix[row]]


def _eliminate_column(matrix: Matrix, row: int, pivot_idx: int) -> None:
    for i, actual_row in enumerate(matrix):
        if i != row:
            multiplier = actual_row[pivot_idx]
            matrix[i] = [
                actual_row_value - pivot_row_value * multiplier
                for actual_row_value, pivot_row_value in zip(actual_row, matrix[row])
            ]


def transform(matrix: Matrix, vector: Vector) -> Vector:
    n = len(vector)
    result = [0.0] * n
    for i in range(n):
        for j in range(n):
            result[i] += matrix[i][j] * vector[j]
    return result


def multiply(left: Matrix, right: Matrix) -> Matrix:
    n = len(left)
    result = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += left[i][k] * right[k][j]
    return result
