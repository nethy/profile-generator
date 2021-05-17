import math
from collections.abc import Sequence

from profile_generator.unit import Point

WeightedPoints = Sequence[tuple[Point, float]]


def get_point_at(control_points: WeightedPoints, t: float) -> Point:
    n = len(control_points) - 1
    b = lambda i, t: math.comb(n, i) * math.pow(t, i) * math.pow((1 - t), n - i)
    weight = 0.0
    result = Point(0, 0)
    for i, (p, w) in enumerate(control_points):
        weight += b(i, t) * w
        result += b(i, t) * p * w
    return result / weight
