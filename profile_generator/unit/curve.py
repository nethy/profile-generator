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


def as_points_multiple(
    curve: Callable[[float], list[float]],
) -> Sequence[Sequence[Point]]:
    prevs = [Point(0, y) for y in curve(0)]
    points: list[list[Point]] = [[prev] for prev in prevs]
    for i in range(1, 255):
        currents = [Point(i / 255, y) for y in curve(i / 255)]
        distance = max(prev.distance(current) for prev, current in zip(prevs, currents))
        if not distance < _TOLERANCE:
            _append_multiple(points, currents)
            prevs = currents
    currents = [Point(1, y) for y in curve(1)]
    _append_multiple(points, currents)
    return points


def _append_multiple(points: list[list[Point]], currents: list[Point]) -> None:
    for i, current in enumerate(currents):
        points[i].append(current)


_POINT_COUNT = 32


def as_fixed_points(curve: Curve) -> Sequence[Point]:
    return [
        Point(i / _POINT_COUNT, curve(i / _POINT_COUNT))
        for i in range(_POINT_COUNT + 1)
    ]


def invert_y(curve: Curve) -> Curve:
    return lambda x: 1 - curve(x)
