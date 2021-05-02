import unittest

from .line import Line
from .point import Point


class LineTest(unittest.TestCase):
    def test_intersection(self) -> None:
        a = Line.from_points(Point(0, 0), Point(1, 1))
        b = Line.from_points(Point(0, 1), Point(1, 0))

        result = a.intersect(b)

        self.assertEqual(Point(0.5, 0.5), result)

    def test_repr(self) -> None:
        self.assertEqual(
            "Line(gradient=1.00000, offset=0.00000)", Line(1, 0).__repr__()
        )
