from unittest import TestCase

from .raw_therapee import Point, present_curve, present_equalizer


class TestRawTherapee(TestCase):
    def test_present_curve(self) -> None:
        self.assertEqual("", present_curve([]))

        self.assertEqual("0.200000;0.800000;", present_curve([Point(0.2, 0.8)]))

        curve = [Point(0, 0), Point(1, 1)]
        self.assertEqual("0.000000;0.000000;1.000000;1.000000;", present_curve(curve))

    def test_present_equalizer(self) -> None:
        self.assertEqual("", present_equalizer([]))

        self.assertEqual(
            "0.000000;0.000000;0.288675;0.288675;1.000000;1.000000;0.288675;0.288675;",
            present_equalizer([Point(0, 0), Point(1, 1)]),
        )
