import math
from collections.abc import Sequence
from functools import cache

from profile_generator.unit import Curve, Point
from profile_generator.util import search

WeightedPoints = Sequence[tuple[Point, float]]


def as_uniform_points(coordinates: Sequence[tuple[float, float]]) -> WeightedPoints:
    return list(
        (p, 1.0) for p in (
            Point(x, y) for x, y in coordinates
        )
    )


def curve(control_points: WeightedPoints, table_size: int = 16) -> Curve:
    def x_at(t: float) -> float:
        return get_point_at(control_points, t).x

    table = search.get_table(0, 1, table_size, x_at)

    @cache
    def _curve(x: float) -> float:
        t = search.table_search(table, x_at, x)
        return get_point_at(control_points, t).y

    return _curve


def get_point_at(control_points: WeightedPoints, t: float) -> Point:
    n = len(control_points) - 1

    def _get_coeffient(i: int, t: float) -> float:
        return math.comb(n, i) * math.pow(t, i) * math.pow((1 - t), n - i)

    weight = 0.0
    result = Point(0, 0)
    for i, (p, w) in enumerate(control_points):
        b = _get_coeffient(i, t)
        weight += b * w
        result += b * p * w
    return result / weight


def get_control_point_coefficent(gradient: float) -> float:
    if gradient < 1 and not math.isclose(gradient, 1):
        raise ValueError(
            "Gradient for bezier control point coefficient must be at least 1."
        )
    return 0.5 * (gradient - 1) / gradient
