import bisect
from collections.abc import Callable, Sequence
from math import pi

from profile_generator.unit.precision import equals

Matrix = list[list[float]]
Vector = list[float]
Point = tuple[float, float]

EPSILON = 1 / 256


def fit(fn: Callable[[float], float]) -> Sequence[Point]:
    ref_values = [fn(x / 255) for x in range(256)]
    points: list[Point] = [(0, ref_values[0]), (1, ref_values[-1])]
    for _ in range(3, 24 + 1):
        spline = interpolate(points)
        max_diff, point = _find_max_diff(ref_values, spline)
        if max_diff > EPSILON:
            bisect.insort(points, point)
        else:
            break
    return points


def _find_max_diff(
    ref_values: Sequence[float], spline: Callable[[float], float]
) -> tuple[float, Point]:
    max_diff, point = 0.0, (0.0, 0.0)
    for i, y in enumerate(ref_values):
        x = i / 255
        diff = abs(y - spline(x))
        if diff > max_diff:
            max_diff, point = diff, (x, y)
    return (max_diff, point)


def interpolate(points: Sequence[Point]) -> Callable[[float], float]:
    if len(points) == 0:
        return lambda _: _raise_value_out_of_domain_error()
    x_knots, y_knots = [x for x, _ in points], [y for _, y in points]
    coefficients, values = _equations(x_knots, y_knots)
    solution = solve(coefficients, values)
    return lambda x: _spline(x, x_knots, solution)


def _equations(x_knots: Vector, y_knots: Vector) -> tuple[Matrix, Vector]:
    n = len(x_knots)
    coefficients = [[0.0 for _ in range((n - 1) * 4)] for _ in range((n - 1) * 4)]
    values = [0.0 for _ in range((n - 1) * 4)]
    _fn_equations(coefficients, values, x_knots, y_knots)
    _dx_equations(coefficients, x_knots)
    _second_dx_equations(coefficients, x_knots)
    _boundaries(coefficients, x_knots)
    return (coefficients, values)


def _fn_equations(
    coefficients: Matrix, values: Vector, x_knots: Vector, y_knots: Vector
) -> None:
    n = len(x_knots)
    for i in range(n - 1):
        x, y = x_knots[i], y_knots[i]
        coefficients[i * 2][i * 4 : (i + 1) * 4] = [x ** 3, x ** 2, x, 1]
        values[i * 2] = y
        x, y = x_knots[i + 1], y_knots[i + 1]
        coefficients[i * 2 + 1][i * 4 : (i + 1) * 4] = [x ** 3, x ** 2, x, 1]
        values[i * 2 + 1] = y


def _dx_equations(coefficients: Matrix, x_knots: Vector) -> None:
    n = len(x_knots)
    for i in range(n - 2):
        x = x_knots[i + 1]
        offset = 2 * (n - 1)
        coefficients[offset + i][i * 4 : (i + 2) * 4] = [
            3 * x ** 2,
            2 * x,
            1,
            0,
            -3 * x ** 2,
            -2 * x,
            -1,
            0,
        ]


def _second_dx_equations(coefficients: Matrix, x_knots: Vector) -> None:
    n = len(x_knots)
    for i in range(n - 2):
        x = x_knots[i + 1]
        offset = 3 * (n - 1) - 1
        coefficients[offset + i][i * 4 : (i + 2) * 4] = [
            6 * x,
            2,
            0,
            0,
            -6 * x,
            -2,
            0,
            0,
        ]


def _boundaries(coefficients: Matrix, x_knots: Vector) -> None:
    n = len(x_knots)
    x = x_knots[0]
    coefficients[-2][:2] = [6 * x, 2]
    x = x_knots[-1]
    coefficients[-1][(n - 2) * 4 : (n - 2) * 4 + 2] = [6 * x, 2]


def _spline(x: float, knots: Sequence[float], coefficients: Sequence[float]) -> float:
    if not knots[0] <= x <= knots[-1]:
        _raise_value_out_of_domain_error()
    index = max(0, bisect.bisect_left(knots, x) - 1)
    a, b, c, d = coefficients[index * 4 : index * 4 + 4]
    return a * x ** 3 + b * x ** 2 + c * x + d


def _raise_value_out_of_domain_error() -> float:
    raise ValueError("Value out of domain error")


def solve(coefficients: Matrix, constants: Vector) -> Vector:
    system = _system_of(coefficients, constants)
    rank = len(system)
    for pivot_idx in range(rank):
        _swap_row(system, pivot_idx)
        _normalize(system[pivot_idx], pivot_idx)
        _eliminate_column(system, pivot_idx)

    return [line[-1] for line in system]


def _system_of(coefficients: Matrix, constants: Vector) -> Matrix:
    return [
        [float(e) for e in line] + [float(constants[i])]
        for i, line in enumerate(coefficients)
    ]


def _swap_row(system: Matrix, pivot_idx: int) -> None:
    if not equals(system[pivot_idx][pivot_idx], 0):
        return

    other_index = pivot_idx
    while other_index < len(system) and equals(system[other_index][pivot_idx], 0):
        other_index += 1

    if other_index == len(system):
        raise ValueError("Unsolvable system error")

    system[pivot_idx], system[other_index] = system[other_index], system[pivot_idx]


def _normalize(line: Vector, pivot_idx: int) -> None:
    divisor = line[pivot_idx]
    line[pivot_idx] = 1.0
    for i in range(pivot_idx + 1, len(line)):
        line[i] = line[i] / divisor


def _eliminate_column(system: Matrix, pivot_idx: int) -> None:
    rank = len(system)
    for i in range(rank):
        if i == pivot_idx:
            continue
        _eliminate(system[i], system[pivot_idx], pivot_idx)


def _eliminate(actual_row: Vector, pivot_row: Vector, pivot_idx: int) -> None:
    multiplier = actual_row[pivot_idx] / pivot_row[pivot_idx]
    actual_row[pivot_idx] = 0.0
    for i in range(pivot_idx + 1, len(actual_row)):
        actual_row[i] = actual_row[i] - pivot_row[i] * multiplier
