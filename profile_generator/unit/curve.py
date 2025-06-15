from collections.abc import Callable
from typing import Sequence

from .point import Point

Curve = Callable[[float], float]

_TOLERANCE = 12 / 256


def as_points(curve: Curve) -> Sequence[Point]:
    prev = Point(0, curve(0))
    points: list[Point] = [prev]
    for i in range(1, 255):
        current = Point(i / 255, curve(i / 255))
        distance = prev.distance(current)
        if not distance < _TOLERANCE:
            points.append(current)
            prev = current
    points.append(Point(1, curve(1)))
    return points


_POINT_COUNT = 32


def as_fixed_points(curve: Curve) -> Sequence[Point]:
    return [
        Point(i / _POINT_COUNT, curve(i / _POINT_COUNT))
        for i in range(_POINT_COUNT + 1)
    ]
