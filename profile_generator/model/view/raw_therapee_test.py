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

        self.assertEqual(present_curve(CurveType.STANDARD, []), "0;")

        self.assertEqual(
            present_curve(CurveType.STANDARD, [Point(0.2, 0.8)]),
            "1;0.2000000;0.8000000;",
        )

        curve = [Point(0, 0), Point(1, 1)]
        self.assertEqual(
            present_curve(CurveType.FLEXIBLE, curve),
            "4;0.0000000;0.0000000;1.0000000;1.0000000;",
        )

    def test_present_equalizer(self) -> None:
        self.assertEqual(present_equalizer([]), "0;")

        self.assertEqual(
            present_equalizer(
                [
                    EqPoint(0, 0),
                    LeftLinearEqPoint(0.4, 0.4),
                    RightLinearEqPoint(0.6, 0.6),
                    LinearEqPoint(1, 1),
                ]
            ),
            "1;0.0000000;0.0000000;0.2500000;0.2500000;"
            + "0.4000000;0.4000000;0.0000000;0.5000000;"
            + "0.6000000;0.6000000;0.5000000;0.0000000;"
            + "1.0000000;1.0000000;0.0000000;0.0000000;",
        )
