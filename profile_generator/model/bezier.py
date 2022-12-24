import math
from collections.abc import Sequence
from functools import cache

from profile_generator.unit import Curve, Point
from profile_generator.util import search

WeightedPoints = Sequence[tuple[Point, float]]


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
