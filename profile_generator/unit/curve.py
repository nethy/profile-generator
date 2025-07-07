from collections.abc import Callable
from typing import Sequence

from profile_generator.model import hermite

from .point import Point

Curve = Callable[[float], float]

_TOLERANCE = 12 / 256


def as_points(curve: Curve) -> Sequence[Point]:
    return [Point(x, y) for x, y in hermite.fit(curve)]


_POINT_COUNT = 32


def as_fixed_points(curve: Curve) -> Sequence[Point]:
    return [
        Point(i / _POINT_COUNT, curve(i / _POINT_COUNT))
        for i in range(_POINT_COUNT + 1)
    ]


def invert_y(curve: Curve) -> Curve:
    return lambda x: 1 - curve(x)
