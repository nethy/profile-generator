from __future__ import annotations

import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: Point) -> float:
        diff_x = self.x - other.x
        diff_y = self.y - other.y
        return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))

    def __repr__(self) -> str:
        return f"Point(x={self.x:.3f}, y={self.y:.3f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return abs(self.x - other.x) < 0.00001 and abs(self.y - other.y) < 0.00001

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