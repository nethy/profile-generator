import bisect
import math
from collections.abc import Callable, Mapping, Sequence

Matrix = list[list[float]]
Vector = list[float]
Point = tuple[float, float]

EPSILON = 1 / 256


def spline_of(fn: Callable[[float], float]) -> Sequence[Point]:
    ref_values = [fn(x / 255) for x in range(256)]
    points: list[Point] = [(0, ref_values[0]), (1, ref_values[-1])]
    for _ in range(3, 24 + 1):
        spline = interpolate(points)
        max_diff, point = _find_max_diff(ref_values, spline)
        if max_diff > EPSILON:
            index = bisect.bisect_left(points, point)
            points.insert(index, point)
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
    coefficients, constants = _equations(points)
    solution = solve(coefficients, constants)
    interpolation = {
        (points[i][0], points[i + 1][0]): solution[i * 4 : (i + 1) * 4]
        for i in range(len(points) - 1)
    }
    return lambda x: value_of(interpolation, x)


def _equations(points: Sequence[Point]) -> tuple[Matrix, Vector]:
    coefficients = []
    constants = []
    n = len(points)
    for i in range(n - 1):
        coeffs, y = _equation(points[i], i, n)
        coefficients.append(coeffs)
        constants.append(y)
        coeffs, y = _equation(points[i + 1], i, n)
        coefficients.append(coeffs)
        constants.append(y)
    for i in range(1, n - 1):
        coeffs, y = _dx_equation(points[i], i - 1, n)
        coefficients.append(coeffs)
        constants.append(y)
    for i in range(1, n - 1):
        coeffs, y = _second_dx_equation(points[i], i - 1, n)
        coefficients.append(coeffs)
        constants.append(y)
    coeffs, y = _second_dx_is_zero(points[0], 0, n)
    coefficients.append(coeffs)
    constants.append(y)
    coeffs, y = _second_dx_is_zero(points[n - 1], n - 2, n)
    coefficients.append(coeffs)
    constants.append(y)
    return (coefficients, constants)


def _equation(point: Point, i: int, n: int) -> tuple[Vector, float]:
    x, y = point
    pos = i * 4
    row: list[float] = [0] * ((n - 1) * 4)
    row[pos : pos + 4] = [x ** 3, x ** 2, x, 1]
    return (row, y)


def _dx_equation(point: Point, i: int, n: int) -> tuple[Vector, float]:
    x, _ = point
    pos = i * 4
    next_pos = (i + 1) * 4
    row: list[float] = [0] * ((n - 1) * 4)
    row[pos : pos + 3] = [3 * x ** 2, 2 * x, 1]
    row[next_pos : next_pos + 3] = [-3 * x ** 2, -2 * x, -1]
    return (row, 0)


def _second_dx_equation(point: Point, i: int, n: int) -> tuple[Vector, float]:
    x, _ = point
    pos = i * 4
    next_pos = (i + 1) * 4
    row: list[float] = [0] * ((n - 1) * 4)
    row[pos : pos + 2] = [6 * x, 2]
    row[next_pos : next_pos + 2] = [-6 * x, -2]
    return (row, 0)


def _second_dx_is_zero(point: Point, i: int, n: int) -> tuple[Vector, float]:
    x, _ = point
    pos = i * 4
    row: list[float] = [0] * ((n - 1) * 4)
    row[pos : pos + 2] = [6 * x, 2]
    return (row, 0)


def value_of(
    interpolation: Mapping[tuple[float, float], Sequence[float]], x: float
) -> float:
    items = sorted(interpolation.items())
    for item in items:
        (low, high), coeffs = item
        if low <= x <= high:
            return coeffs[0] * x ** 3 + coeffs[1] * x ** 2 + coeffs[2] * x + coeffs[3]
    return _raise_value_out_of_domain_error()


def _raise_value_out_of_domain_error() -> float:
    raise ValueError("Value out of domain error")


def solve(coefficients: Matrix, constants: Vector) -> Vector:
    system = _system_of(coefficients, constants)
    rank = len(system)
    for pivot_idx in range(rank):
        _swap_row(system, pivot_idx)
        _normalize(system[pivot_idx], pivot_idx)
        _eliminate_column(system, rank, pivot_idx)

    return [line[-1] for line in system]


def _system_of(coefficients: Matrix, constants: Vector) -> Matrix:
    return [
        [float(e) for e in line] + [float(constants[i])]
        for i, line in enumerate(coefficients)
    ]


def _swap_row(system: Matrix, pivot_idx: int) -> None:
    if not math.isclose(system[pivot_idx][pivot_idx], 0):
        return

    other_index = pivot_idx
    while other_index < len(system) and math.isclose(system[other_index][pivot_idx], 0):
        other_index += 1

    if other_index == len(system):
        raise ValueError("Unsolvable system error")

    system[pivot_idx], system[other_index] = system[other_index], system[pivot_idx]


def _normalize(line: Vector, pivot_idx: int) -> None:
    multiplier = 1.0 / line[pivot_idx]
    for i in range(pivot_idx, len(line)):
        line[i] = line[i] * multiplier


def _eliminate_column(system: Matrix, rank: int, pivot_idx: int) -> None:
    for i in range(rank):
        if i == pivot_idx:
            continue
        _eliminate(system[i], system[pivot_idx], pivot_idx)


def _eliminate(actual: Vector, pivot_row: Vector, pivot_idx: int) -> None:
    multiplier = actual[pivot_idx] / pivot_row[pivot_idx]
    for i in range(pivot_idx, len(actual)):
        actual[i] = actual[i] - pivot_row[i] * multiplier
