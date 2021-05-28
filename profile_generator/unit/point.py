from __future__ import annotations

import math
from collections.abc import Iterator

from .precision import DECIMALS, equals


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: Point) -> float:
        diff_x = self.x - other.x
        diff_y = self.y - other.y
        return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))

    def __repr__(self) -> str:
        return f"Point(x={self.x:.{DECIMALS}f}, y={self.y:.{DECIMALS}f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return equals(self.x, other.x) and equals(self.y, other.y)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return not self.__eq__(other)

    def __add__(self, operand: Point) -> Point:
        return Point(self.x + operand.x, self.y + operand.y)

    __radd__ = __add__

    __iadd__ = __add__

    def __mul__(self, operand: float) -> Point:
        return Point(self.x * operand, self.y * operand)

    __rmul__ = __mul__

    def __truediv__(self, other: float) -> Point:
        return Point(self.x / other, self.y / other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
