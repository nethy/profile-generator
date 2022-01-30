from unittest import TestCase

from .raw_therapee import (
    CurveType,
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
        self.assertEqual(present_curve(CurveType.LINEAR, []), "0;")

        self.assertEqual(
            present_curve(CurveType.STANDARD, [Point(0.2, 0.8)]), "1;0.200000;0.800000;"
        )

        curve = [Point(0, 0), Point(1, 1)]
        self.assertEqual(
            present_curve(CurveType.FLEXIBLE, curve),
            "4;0.000000;0.000000;1.000000;1.000000;",
        )

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
            "0.000000;0.000000;0.250000;0.250000;"
            + "0.400000;0.400000;0.000000;0.500000;"
            + "0.600000;0.600000;0.500000;0.000000;"
            + "1.000000;1.000000;0.000000;0.000000;",
        )
