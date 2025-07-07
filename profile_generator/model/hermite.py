import bisect
import math
from collections.abc import Callable, Sequence

Points = list[tuple[float, float]]

_EPSILON = 1 / 256


def fit(fn: Callable[[float], float]) -> Points:
    references = [(i / 255, fn(i / 255)) for i in range(1, 255)]
    knots = [(0.0, fn(0.0)), (1.0, fn(1.0))]
    max_diff, _ = _find_max_diff(references, knots)
    if max_diff < _EPSILON:
        return knots
    _fit(references, knots)
    return knots


def _find_max_diff(references: Points, knots: Points) -> tuple[float, int]:
    spline = interpolate(knots)
    return max((abs(p[1] - spline(p[0])), i) for i, p in enumerate(references))


def _fit(references: Points, knots: Points) -> None:
    for _ in range(31):
        max_diff, i = _find_max_diff(references, knots)
        if max_diff < _EPSILON:
            break
        bisect.insort(knots, references.pop(i))


def interpolate(points: Sequence[tuple[float, float]]) -> Callable[[float], float]:
    secants = []
    for i in range(len(points) - 1):
        secants.append(
            (points[i + 1][1] - points[i][1]) / (points[i + 1][0] - points[i][0])
        )

    slopes = [secants[0]]
    for i in range(1, len(points) - 1):
        slopes.append((secants[i - 1] + secants[i]) / 2)
    slopes.append(secants[-1])

    for i in range(0, len(points) - 1):
        if math.isclose(secants[i], 0):
            slopes[i] = slopes[i + 1] = 0
        else:
            alpha = slopes[i] / secants[i]
            beta = slopes[i + 1] / secants[i]
            h = math.hypot(alpha, beta)
            if h > 3:
                t = 3 / h
                slopes[i] = t * alpha * secants[i]
                slopes[i + 1] = t * beta * secants[i]

    def curve(x: float) -> float:
        if x <= points[0][0]:
            return points[0][1]
        if x >= points[-1][0]:
            return points[-1][1]

        i = 0
        while points[i + 1][0] <= x:
            i += 1
        return hermite_interpolate(
            x, points[i], points[i + 1], slopes[i], slopes[i + 1]
        )

    return curve


def hermite_interpolate(
    x: float,
    left: tuple[float, float],
    right: tuple[float, float],
    left_slope: float,
    right_slope: float,
) -> float:
    h = right[0] - left[0]
    t = (x - left[0]) / h
    return (left[1] * (1 + 2 * t) + h * left_slope * t) * math.pow(1 - t, 2) + (
        right[1] * (3 - 2 * t) + h * right_slope * (t - 1)
    ) * math.pow(t, 2)
