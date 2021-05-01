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

    @staticmethod
    def _eq(a: float, b: float) -> bool:
        return abs(a - b) < _PRECISION

    def for_raw_therapee(self) -> str:
        return f"{self.x:.5f};{self.y:.5f};{self.left:.5f};{self.right:.5f};"


def equalize(*points: Point) -> list[EqPoint]:
    if len(points) == 0:
        return []
    result = [EqPoint(p.x, p.y, 0, 0) for p in points]
    for i in range(len(result) - 1):
        strength = _get_slope_strength(result[i], result[i + 1])
        _set_slope_strength(result[i], result[i + 1], strength)
    strength = _get_slope_strength(result[-1], _transpose(points[0]))
    _set_slope_strength(result[-1], result[0], strength)
    return result


def _get_slope_strength(a: EqPoint, b: EqPoint) -> float:
    if a.x == b.x or a.y == b.y:
        return 0
    slope = abs((b.y - a.y) / (b.x - a.x))
    return (1 - 1 / math.exp(2 * slope)) / 2


def _set_slope_strength(left: EqPoint, right: EqPoint, strength: float) -> None:
    left.right = strength
    right.left = strength


def _transpose(point: Point) -> EqPoint:
    return EqPoint(point.x + 1, point.y, 0, 0)
