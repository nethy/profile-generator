import unittest
from functools import partial

from profile_generator.unit import Point

from . import bezier


class BezierTest(unittest.TestCase):
    def test_get_point_at(self) -> None:
        control_points = [(Point(0, 0), 1), (Point(0.2, 0), 2), (Point(0.5, 0.5), 1)]
        bezier_at = partial(bezier.get_point_at, control_points)

        self.assertEqual(Point(0, 0), bezier_at(0))
        self.assertEqual(Point(0.131818, 0.022727), bezier_at(0.25))
        self.assertEqual(Point(0.216667, 0.083333), bezier_at(0.5))
        self.assertEqual(Point(0.313636, 0.204545), bezier_at(0.75))
        self.assertEqual(Point(0.5, 0.5), bezier_at(1))
