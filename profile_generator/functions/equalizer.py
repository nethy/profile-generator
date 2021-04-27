from __future__ import annotations

import math
from dataclasses import dataclass

from profile_generator.unit import Point

_PRECISION = 0.00001


@dataclass
class EqPoint:
    x: float
    y: float
    left: float
    right: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EqPoint):
            return NotImplemented
        return (
            self._eq(self.x, other.x)
            and self._eq(self.y, other.y)
            and self._eq(self.left, other.left)
            and self._eq(self.right, other.right)
        )

    def _eq(self, a: float, b: float) -> bool:
        return abs(a - b) < _PRECISION


def equalize(*points: Point) -> list[EqPoint]:
    result = [EqPoint(p.x, p.y, 0, 0) for p in points]
    for i in range(len(result) - 1):
        strength = _get_slope_strength(result[i], result[i + 1])
        result[i].right = strength
        result[i + 1].left = strength
    return result


def _get_slope_strength(a: EqPoint, b: EqPoint) -> float:
    if a.x == b.x or a.y == b.y:
        return 0
    slope = abs((b.y - a.y) / (b.x - a.x))
    return (1 - math.exp(-2 * slope)) / 2
