from collections.abc import Callable
from typing import Sequence

from .point import Point

Curve = Callable[[float], float]

_TOLERANCE = 0.05


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


def as_fixed_points(curve: Curve) -> Sequence[Point]:
    return [Point(i / (64 - 1), curve(i / (64 - 1))) for i in range(64)]
