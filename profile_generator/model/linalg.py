import math
from collections.abc import Callable
from decimal import Decimal

from profile_generator.unit import Matrix, Vector


def vector_length(vector: Vector) -> float:
    return math.sqrt(sum((math.pow(i, 2) for i in vector)))


def solve(matrix: Matrix) -> Vector:
    system = [[Decimal(i) for i in line] for line in matrix]
    _inverse(system)
    return [float(line[-1]) for line in system]


def inverse(matrix: Matrix) -> Matrix:
    unit_matrix = [[Decimal(0)] * len(matrix) for _ in range(len(matrix))]
    for i, row in enumerate(unit_matrix):
        row[i] = Decimal(1)
    system = [
        [Decimal(i) for i in row] + unit_row
        for row, unit_row in zip(matrix, unit_matrix)
    ]
    _inverse(system)
    return [[float(i) for i in row[len(system) :]] for row in system]


def _inverse(matrix: list[list[Decimal]]) -> None:
    pivot_idx = 0
    for row in range(len(matrix)):
        if not pivot_idx < len(matrix[0]):
            break
        pivot_idx = _swap_row(matrix, row, pivot_idx)
        if pivot_idx < len(matrix[0]):
            _normalize(matrix, row, pivot_idx)
            _eliminate_column(matrix, row, pivot_idx)
            pivot_idx += 1


def _swap_row(matrix: list[list[Decimal]], row: int, pivot_idx: int) -> int:
    i = row
    while pivot_idx < len(matrix[0]) and math.isclose(matrix[i][pivot_idx], 0):
        i += 1
        if i == len(matrix):
            i = row
            pivot_idx += 1

    if i < len(matrix):
        matrix[row], matrix[i] = matrix[i], matrix[row]

    return pivot_idx


def _normalize(matrix: list[list[Decimal]], row: int, pivot_idx: int) -> None:
    divisor = matrix[row][pivot_idx]
    matrix[row] = [value / divisor for value in matrix[row]]


def _eliminate_column(matrix: list[list[Decimal]], row: int, pivot_idx: int) -> None:
    for i, actual_row in enumerate(matrix):
        if i != row:
            multiplier = actual_row[pivot_idx]
            matrix[i] = [
                actual_row_value - pivot_row_value * multiplier
                for actual_row_value, pivot_row_value in zip(actual_row, matrix[row])
            ]


def multiply_matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    n = len(vector)
    result = [0.0] * n
    for i in range(n):
        for j in range(n):
            result[i] += matrix[i][j] * vector[j]
    return result


def multiply_vector_vector(left: Vector, right: Vector) -> float:
    return sum(a * b for a, b in zip(left, right))


def multiply_matrix_matrix(left: Matrix, right: Matrix) -> Matrix:
    n = len(left)
    result = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += left[i][k] * right[k][j]
    return result


def scale_matrix(scale: Vector, matrix: Matrix) -> Matrix:
    return [[a * x for x in row] for a, row in zip(scale, matrix)]


def add_vectors(a: Vector, b: Vector) -> Vector:
    return [a_value + b_value for a_value, b_value in zip(a, b)]


def multiply_vector(a: Vector, scalar: float) -> Vector:
    return [scalar * value for value in a]


def add_vector(a: Vector, scalar: float) -> Vector:
    return [scalar + value for value in a]


def map_vector(a: Vector, fn: Callable[[float], float]) -> Vector:
    return [fn(value) for value in a]
