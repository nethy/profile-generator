from __future__ import annotations

from .point import Point
from .precision import DECIMALS, equals


class Line:
    def __init__(self, gradient: float, offset: float):
        self.gradient = gradient
        self.offset = offset

    @staticmethod
    def from_points(a: Point, b: Point) -> Line:
        gradient = (b.y - a.y) / (b.x - a.x)
        offset = a.y - gradient * a.x
        return Line(gradient, offset)

    @staticmethod
    def at_point(point: Point, gradient: float) -> Line:
        return Line(gradient, point.y - point.x * gradient)

    def __repr__(self) -> str:
        return (
            f"Line(gradient={self.gradient:.{DECIMALS}f}, "
            + f"offset={self.offset:.{DECIMALS}f})"
        )

    def intersect(self, other: Line) -> Point:
        x = (other.offset - self.offset) / (self.gradient - other.gradient)
        y = self.get_y(x)
        return Point(x, y)

    def get_x(self, y: float) -> float:
        return (y - self.offset) / self.gradient

    def get_y(self, x: float) -> float:
        return self.gradient * x + self.offset

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented

        return equals(self.gradient, other.gradient) and equals(
            self.offset, other.offset
        )
