import bisect
import math
from collections.abc import Sequence

from profile_generator.model import linalg
from profile_generator.model.linalg import Matrix, Vector
from profile_generator.unit import Curve, Point

EPSILON = 1e-3
SAMPLES_COUNT = 127


def fit(fn: Curve) -> Sequence[Point]:
    range_end = SAMPLES_COUNT - 1
    references = [(i / range_end, fn(i / range_end)) for i in range(1, range_end)]
    knots = [Point(0.0, fn(0.0)), Point(1.0, fn(1.0))]
    for _ in range(3, 24 + 1):
        spline = interpolate(knots)
        max_diff, i = _find_max_diff(references, spline)
        if max_diff > EPSILON:
            x, y = references.pop(i)
            bisect.insort(knots, Point(x, y))
        else:
            break
    return knots


def _find_max_diff(
    references: list[tuple[float, float]], spline: Curve
) -> tuple[float, int]:
    return max((abs(y - spline(x)), i) for i, (x, y) in enumerate(references))


def interpolate(points: Sequence[Point]) -> Curve:
    if len(points) == 0:
        return lambda x: 0.0
    elif len(points) == 1:
        return lambda x: points[0].y
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
