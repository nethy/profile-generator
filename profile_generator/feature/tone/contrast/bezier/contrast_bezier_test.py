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
                Point(0.04972, 0.03141),
                Point(0.08479, 0.06206),
                Point(0.11581, 0.09724),
                Point(0.14852, 0.14199),
                Point(0.18863, 0.20409),
                Point(0.24548, 0.29917),
                Point(0.34118, 0.46667),
                Point(0.41723, 0.58862),
                Point(0.49931, 0.69532),
                Point(0.58741, 0.78677),
                Point(0.68153, 0.86296),
                Point(0.78166, 0.92389),
                Point(0.88782, 0.96958),
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
                Point(0.13747, 0.01416),
                Point(0.21947, 0.03777),
                Point(0.27770, 0.07161),
                Point(0.32564, 0.11955),
                Point(0.37164, 0.18994),
                Point(0.42436, 0.30104),
                Point(0.50000, 0.50000),
                Point(0.55095, 0.62545),
                Point(0.60873, 0.73289),
                Point(0.67333, 0.82233),
                Point(0.74476, 0.89376),
                Point(0.82301, 0.94718),
                Point(0.90809, 0.98259),
                Point(1, 1),
            ],
            result,
        )
