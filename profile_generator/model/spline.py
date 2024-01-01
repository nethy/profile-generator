import bisect
import math
from collections.abc import Sequence

from profile_generator.model import linalg
from profile_generator.model.linalg import Matrix, Vector
from profile_generator.unit import Curve

BUFFER_SIZE = 8
BUFFER_STEP = 33
SAMPLES_COUNT = (BUFFER_SIZE - 1) * BUFFER_STEP

Points = list[tuple[float, float]]


def fit(
    fn: Curve, start: float = 0.0, end: float = 1.0, epsilon: float = 1e-4
) -> Points:
    if start > end:
        raise ValueError(f"Start {start} must be smaller than end {end}")
    if math.isclose(start, end):
        return [(start, fn(start))]

    references = _generate_references(fn, start, end)
    knots = [(start, fn(start)), (end, fn(end))]
    max_diff, _ = _find_max_diff(references, knots)
    if max_diff < epsilon:
        return knots
    _buffer(references, knots)
    _approximate(references, knots, epsilon)
    return knots


def _generate_references(fn: Curve, start: float, end: float) -> Points:
    length = end - start
    return [
        (start + length * i / SAMPLES_COUNT, fn(start + length * i / SAMPLES_COUNT))
        for i in range(1, SAMPLES_COUNT - 1)
    ]


def _find_max_diff(references: Points, knots: Points) -> tuple[float, int]:
    spline = interpolate(knots)
    return max((abs(p[1] - spline(p[0])), i) for i, p in enumerate(references))


def _buffer(references: Points, knots: Points) -> None:
    for i in range(
        BUFFER_STEP - 1, SAMPLES_COUNT - 2 - BUFFER_SIZE + 1, BUFFER_STEP - 1
    ):
        _transfer_knot(i, references, knots)


def _transfer_knot(
    i: int,
    references: Points,
    knots: Points,
) -> None:
    bisect.insort(knots, references.pop(i))


def _approximate(references: Points, knots: Points, epsilon: float) -> None:
    for _ in range(BUFFER_SIZE + 1, 32 + 1):
        max_diff, i = _find_max_diff(references, knots)
        if max_diff < epsilon:
            break
        _transfer_knot(i, references, knots)


def interpolate(points: Points) -> Curve:
    if len(points) == 0:
        return lambda _: 0.0
    elif len(points) == 1:
        return lambda _: points[0][1]
    xs, ys = [x for x, _ in points], [y for _, y in points]
    system = _equations(xs, ys)
    coefficients = linalg.solve(system)
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
        matrix[i * 2][i * 4 : (i + 1) * 4] = [math.pow(x, 3), math.pow(x, 2), x, 1.0]
        matrix[i * 2][-1] = y
        x, y = xs[i + 1], ys[i + 1]
        matrix[i * 2 + 1][i * 4 : (i + 1) * 4] = [
            math.pow(x, 3),
            math.pow(x, 2),
            x,
            1.0,
        ]
        matrix[i * 2 + 1][-1] = y


def _dx_equations(matrix: Matrix, xs: Vector) -> None:
    n = len(xs)
    for i in range(n - 2):
        x = xs[i + 1]
        offset = 2 * (n - 1)
        matrix[offset + i][i * 4 : (i + 2) * 4] = [
            3 * math.pow(x, 2),
            2 * x,
            1.0,
            0.0,
            -3 * math.pow(x, 2),
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
    a, b, c, d = _find_coeffs(x, knots, coefficients)
    return a * math.pow(x, 3) + b * math.pow(x, 2) + c * x + d


def _find_coeffs(x: float, knots: Vector, coefficients: Vector) -> Sequence[float]:
    for i in range(len(knots) - 1):
        if (
            knots[i] < x < knots[i + 1]
            or math.isclose(x, knots[i])
            or math.isclose(x, knots[i + 1])
        ):
            return coefficients[i * 4 : (i + 1) * 4]
    return [0.0, 0.0, 0.0, 0.0]
