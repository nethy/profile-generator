from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate, calculate_with_hl_protection

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.086275, y=0.046874),
                Point(x=0.203922, y=0.189929),
                Point(x=0.396078, y=0.580512),
                Point(x=0.564706, y=0.831159),
                Point(x=0.776471, y=0.957846),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _STRENGTH),
        )

    def test_calculate_linear(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(1.00000, 1.00000),
            ],
            calculate(Point(0.5, 0.5), Strength()),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.078431, y=0.087183),
                Point(x=0.207843, y=0.207521),
                Point(x=0.400000, y=0.583295),
                Point(x=0.556863, y=0.797609),
                Point(x=0.776471, y=0.897014),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.074510, y=0.038120),
                Point(x=0.188235, y=0.164637),
                Point(x=0.294118, y=0.365240),
                Point(x=0.356863, y=0.500110),
                Point(x=0.529412, y=0.741970),
                Point(x=0.733333, y=0.889626),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.078431, y=0.087183),
                Point(x=0.196078, y=0.190810),
                Point(x=0.286275, y=0.347719),
                Point(x=0.360784, y=0.503005),
                Point(x=0.525490, y=0.715693),
                Point(x=0.737255, y=0.840661),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
