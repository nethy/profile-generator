import bisect
from collections.abc import Callable, Sequence

from profile_generator.unit import equals

Matrix = list[list[float]]
Vector = list[float]
Point = tuple[float, float]

EPSILON = 1 / 2048


def fit(fn: Callable[[float], float]) -> Sequence[Point]:
    values = [(x / 255, fn(x / 255)) for x in range(256)]
    knots: list[Point] = [(0.0, values[0][1]), (1.0, values[-1][1])]
    for _ in range(3, 24 + 1):
        spline = interpolate(knots)
        max_diff, point, idx = _find_max_diff(values, spline)
        if max_diff > EPSILON:
            bisect.insort(knots, point)
            del values[idx]
        else:
            break
    return knots


def _find_max_diff(
    values: list[Point], spline: Callable[[float], float]
) -> tuple[float, Point, int]:
    return max(((abs(y - spline(x)), (x, y), i) for i, (x, y) in enumerate(values)))


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
    pivot_idx = 0
    for row in range(len(system)):
        if not pivot_idx < len(system[0]):
            break
        pivot_idx = _swap_row(system, row, pivot_idx)
        if pivot_idx < len(system[0]):
            _normalize(system, row, pivot_idx)
            _eliminate_column(system, row, pivot_idx)
            pivot_idx += 1
    return [line[-1] for line in system]


def _system_of(coefficients: Matrix, constants: Vector) -> Matrix:
    return [
        [float(e) for e in line] + [float(constants[i])]
        for i, line in enumerate(coefficients)
    ]


def _swap_row(system: Matrix, row: int, pivot_idx: int) -> int:
    i = row
    while pivot_idx < len(system[0]) and equals(system[i][pivot_idx], 0):
        i += 1
        if i == len(system):
            i = row
            pivot_idx += 1

    if i < len(system):
        system[row], system[i] = system[i], system[row]

    return pivot_idx


def _normalize(system: Matrix, row: int, pivot_idx: int) -> None:
    divisor = system[row][pivot_idx]
    system[row] = [value / divisor for value in system[row]]


def _eliminate_column(system: Matrix, row: int, pivot_idx: int) -> None:
    for i, actual_row in enumerate(system):
        if i != row:
            multiplier = actual_row[pivot_idx]
            system[i] = [
                actual_row_value - pivot_row_value * multiplier
                for actual_row_value, pivot_row_value in zip(actual_row, system[row])
            ]
