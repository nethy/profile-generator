import math
from unittest import TestCase

from .hermite import interpolate


class HermiteTest(TestCase):
    def test_interpolate(self) -> None:
        curve = interpolate([(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)])

        self.assertEqual(curve(0), 0)
        self.assertEqual(curve(1), 1)
        self.assertEqual(curve(2), 4)
        self.assertEqual(curve(3), 9)
        self.assertEqual(curve(4), 16)

        self.assertEqual(curve(-1), 0)
        self.assertEqual(curve(5), 16)

        self.assertEqual(curve(1.5), math.pow(1.5, 2))
        self.assertEqual(curve(2.5), math.pow(2.5, 2))
        self.assertEqual(curve(3.5), math.pow(3.5, 2) + 0.125)
