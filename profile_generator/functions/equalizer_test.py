from unittest import TestCase

from .equalizer import EqPoint, Point, equalize


class EqualizerTest(TestCase):
    def test_equalize_linear(self) -> None:
        points = equalize(Point(0, 0.5), Point(1, 0.5))
        self.assertEqual([EqPoint(0, 0.5, 0, 0), EqPoint(1, 0.5, 0, 0)], points)

    def test_equalize(self) -> None:
        self.assertEqual(
            [EqPoint(0, 1, 0, 0.43233), EqPoint(1, 0, 0.43233, 0)],
            equalize(Point(0, 1), Point(1, 0)),
        )

        self.assertEqual(
            [
                EqPoint(0, 1, 0, 0.49084),
                EqPoint(0.5, 0, 0.49084, 0.49084),
                EqPoint(1, 1, 0.49084, 0),
            ],
            equalize(Point(0, 1), Point(0.5, 0), Point(1, 1)),
        )
