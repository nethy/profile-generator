from unittest import TestCase

from .raw_therapee import (
    Point,
    present_curve,
    present_equalizer,
    present_linear_equalizer,
)


class TestRawTherapee(TestCase):
    def test_present_curve(self) -> None:
        self.assertEqual(present_curve([]), "")

        self.assertEqual(present_curve([Point(0.2, 0.8)]), "0.200000;0.800000;")

        curve = [Point(0, 0), Point(1, 1)]
        self.assertEqual(present_curve(curve), "0.000000;0.000000;1.000000;1.000000;")

    def test_present_equalizer(self) -> None:
        self.assertEqual(present_equalizer([]), "")

        self.assertEqual(
            present_equalizer([Point(0, 0), Point(1, 1)]),
            "0.000000;0.000000;0.25;0.25;1.000000;1.000000;0.25;0.25;",
        )

    def test_present_linear_equalizer(self) -> None:
        self.assertEqual(
            present_linear_equalizer([Point(0, 0), Point(1, 1)]),
            "0.000000;0.000000;0;0;1.000000;1.000000;0;0;",
        )
