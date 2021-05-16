from unittest import TestCase

from .raw_therapee import EqPoint, Point, present_curve, present_equalizer


class TestRawTherapee(TestCase):
    def test_present_curve(self) -> None:
        self.assertEqual("", present_curve([]))

        self.assertEqual("0.200000;0.800000;", present_curve([Point(0.2, 0.8)]))

        curve = [Point(0, 0), Point(1, 1)]
        self.assertEqual("0.000000;0.000000;1.000000;1.000000;", present_curve(curve))

    def test_present_equalizer(self) -> None:
        self.assertEqual("", present_equalizer([]))

        self.assertEqual(
            "0.200000;0.800000;0.300000;0.400000;",
            present_equalizer([EqPoint(0.2, 0.8, 0.3, 0.4)]),
        )

        equalizer = [EqPoint(0, 0, 0.2, 0.3), EqPoint(1, 1, 0.4, 0.5)]
        self.assertEqual(
            "0.000000;0.000000;0.200000;0.300000;1.000000;1.000000;0.400000;0.500000;",
            present_equalizer(equalizer),
        )
