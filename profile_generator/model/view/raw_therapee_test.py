from unittest import TestCase

from .raw_therapee import (
    EqPoint,
    LeftLinearEqPoint,
    LinearEqPoint,
    Point,
    RightLinearEqPoint,
    present_curve,
    present_equalizer,
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
            present_equalizer(
                [
                    EqPoint(0, 0),
                    LeftLinearEqPoint(0.4, 0.4),
                    RightLinearEqPoint(0.6, 0.6),
                    LinearEqPoint(1, 1),
                ]
            ),
            "0.000000;0.000000;0.333333;0.333333;"
            + "0.400000;0.400000;0.000000;0.333333;"
            + "0.600000;0.600000;0.333333;0.000000;"
            + "1.000000;1.000000;0.000000;0.000000;",
        )
