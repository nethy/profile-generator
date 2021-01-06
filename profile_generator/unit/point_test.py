import math
import unittest

from .point import Point


class PointTest(unittest.TestCase):
    def test_repr(self) -> None:
        point = Point(0.1, 0.2)

        self.assertEqual("Point(x=0.100, y=0.200)", str(point))

    def test_distance(self) -> None:
        a = Point(1, 1)
        b = Point(2, 2)

        self.assertEqual(0, a.distance(a))
        self.assertEqual(a.distance(b), b.distance(a))
        self.assertEqual(math.sqrt(2), a.distance(b))
