from collections.abc import Callable
from typing import Sequence

from .point import Point

Curve = Callable[[float], float]


def as_points(curve: Curve, sample_size: int = 32) -> Sequence[Point]:
    return [
        Point(i / (sample_size - 1), curve(i / (sample_size - 1)))
        for i in range(sample_size)
    ]
