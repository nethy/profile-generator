from unittest import TestCase

from .equalizer import EqPoint, Point, equalize


class EqualizerTest(TestCase):
    def test_equalize_no_point(self) -> None:
        self.assertEqual([], equalize())

    def test_equalize_linear(self) -> None:
        points = equalize(Point(0, 0.5), Point(1, 0.5))
        self.assertEqual([EqPoint(0, 0.5, 0, 0), EqPoint(1, 0.5, 0, 0)], points)

    def test_equalize(self) -> None:
        self.assertEqual(
            [EqPoint(0, 1, 0, 0.375), EqPoint(1, 0, 0.375, 0)],
            equalize(Point(0, 1), Point(1, 0)),
        )

        self.assertEqual(
            [
                EqPoint(0, 1, 0.49805, 0.42125),
                EqPoint(0.75, 0, 0.42125, 0.49805),
            ],
            equalize(Point(0, 1), Point(0.75, 0)),
        )
