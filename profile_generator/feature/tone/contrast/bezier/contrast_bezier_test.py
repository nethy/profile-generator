from unittest import TestCase

from profile_generator.unit import Point, Strength

from . import contrast_bezier


class ContrastBezierTest(TestCase):
    def test_calculate_when_strength_is_less_than_1(self) -> None:
        grey = Point(87 / 255, 119 / 255)
        strength = Strength(0.2)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

        self.assertSequenceEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.034104, y=0.011898),
                Point(x=0.067123, y=0.032046),
                Point(x=0.101173, y=0.062638),
                Point(x=0.138934, y=0.107823),
                Point(x=0.184578, y=0.175511),
                Point(x=0.245956, y=0.282055),
                Point(x=0.341176, y=0.466667),
                Point(x=0.411874, y=0.592823),
                Point(x=0.490379, y=0.702323),
                Point(x=0.576690, y=0.795169),
                Point(x=0.670807, y=0.871359),
                Point(x=0.772732, y=0.930895),
                Point(x=0.882463, y=0.973775),
                Point(x=1.000000, y=1.000000),
            ],
            result,
        )

    def test_calculate_when_strength_is_1(self) -> None:
        grey = Point(0.5, 0.5)
        strength = Strength(1)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

        self.assertSequenceEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.098924, y=0.009097),
                Point(x=0.182546, y=0.028056),
                Point(x=0.254957, y=0.059154),
                Point(x=0.319405, y=0.106887),
                Point(x=0.378895, y=0.179963),
                Point(x=0.437026, y=0.296490),
                Point(x=0.500000, y=0.500000),
                Point(x=0.538894, y=0.624966),
                Point(x=0.588634, y=0.732085),
                Point(x=0.649217, y=0.821360),
                Point(x=0.720646, y=0.892788),
                Point(x=0.802919, y=0.946371),
                Point(x=0.896037, y=0.982108),
                Point(x=1.000000, y=1.000000),
            ],
            result,
        )
