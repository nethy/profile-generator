import unittest
from functools import partial

from profile_generator.unit import Point

from . import bezier


class BezierTest(unittest.TestCase):
    def test_as_uniform_points(self) -> None:
        coordinates = [(0, 0), (1, 1)]

        weighted_points = bezier.as_uniform_points(coordinates)

        self.assertEqual(weighted_points, [(Point(0, 0), 1), (Point(1, 1), 1)])

    def test_curve(self) -> None:
        control_points = [(Point(0, 0), 1), (Point(0, 1), 1), (Point(1, 1), 1)]

        curve = bezier.curve(control_points)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.25), 0.75)
        self.assertAlmostEqual(curve(1), 1)

    def test_get_point_at(self) -> None:
        control_points = [(Point(0, 0), 1), (Point(0.2, 0), 2), (Point(0.5, 0.5), 1)]

        bezier_at = partial(bezier.get_point_at, control_points)

        self.assertEqual(bezier_at(0), Point(0, 0))
        self.assertEqual(Point(0.1318182, 0.0227273), bezier_at(0.25))
        self.assertEqual(Point(0.2166667, 0.0833333), bezier_at(0.5))
        self.assertEqual(Point(0.3136364, 0.2045455), bezier_at(0.75))
        self.assertEqual(Point(0.5, 0.5), bezier_at(1))

    def test_get_control_point_coefficient(self) -> None:
        self.assertRaises(ValueError, lambda: bezier.get_control_point_coefficent(0.99))
        self.assertAlmostEqual(bezier.get_control_point_coefficent(1), 0)
        self.assertAlmostEqual(bezier.get_control_point_coefficent(2), 0.25)
