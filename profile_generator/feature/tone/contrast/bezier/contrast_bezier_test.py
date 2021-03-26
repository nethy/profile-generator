from unittest import TestCase

from profile_generator.unit import Point, Strength

from . import contrast_bezier


class ResolveTest(TestCase):
    def test_calculate_when_strength_is_less_than_1(self) -> None:
        grey = Point(87 / 255, 119 / 255)
        strength = Strength(0.2)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

        self.assertSequenceEqual(
            [
                Point(0, 0),
                Point(0.04314, 0.01974),
                Point(0.07510, 0.04486),
                Point(0.10481, 0.07773),
                Point(0.13753, 0.12248),
                Point(0.17894, 0.18689),
                Point(0.23890, 0.28750),
                Point(0.34118, 0.46667),
                Point(0.41915, 0.59203),
                Point(0.50251, 0.70100),
                Point(0.59125, 0.79358),
                Point(0.68537, 0.86977),
                Point(0.78487, 0.92957),
                Point(0.88974, 0.97298),
                Point(1, 1),
            ],
            result,
        )

    def test_calculate_when_strength_is_1(self) -> None:
        grey = Point(0.5, 0.5)
        strength = Strength(1)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

        self.assertSequenceEqual(
            [
                Point(0, 0),
                Point(0.13831, 0.01652),
                Point(0.22070, 0.04125),
                Point(0.27909, 0.07556),
                Point(0.32704, 0.12350),
                Point(0.37287, 0.19343),
                Point(0.42520, 0.30341),
                Point(0.50000, 0.50000),
                Point(0.54998, 0.62271),
                Point(0.60711, 0.72832),
                Point(0.67139, 0.81685),
                Point(0.74282, 0.88828),
                Point(0.82140, 0.94261),
                Point(0.90712, 0.97985),
                Point(1, 1),
            ],
            result,
        )
