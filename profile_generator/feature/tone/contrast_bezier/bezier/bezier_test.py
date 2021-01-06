import unittest
from functools import partial

from unit import Point

from . import bezier


class BezierTest(unittest.TestCase):
    def test_get_point_at(self) -> None:
        control_points = [(Point(0, 0), 1), (Point(0.2, 0), 2), (Point(0.5, 0.5), 1)]
        bezier_at = partial(bezier.get_point_at, control_points)

        self.assertEqual(Point(0, 0), bezier_at(0))
        self.assertEqual(Point(0.13182, 0.02273), bezier_at(0.25))
        self.assertEqual(Point(0.21667, 0.08333), bezier_at(0.5))
        self.assertEqual(Point(0.31364, 0.20455), bezier_at(0.75))
        self.assertEqual(Point(0.5, 0.5), bezier_at(1))
