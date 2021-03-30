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
                Point(0.03410, 0.01190),
                Point(0.06712, 0.03205),
                Point(0.10117, 0.06264),
                Point(0.13893, 0.10782),
                Point(0.18458, 0.17551),
                Point(0.24596, 0.28205),
                Point(0.34118, 0.46667),
                Point(0.41187, 0.59282),
                Point(0.49038, 0.70232),
                Point(0.57669, 0.79517),
                Point(0.67081, 0.87136),
                Point(0.77273, 0.93089),
                Point(0.88246, 0.97377),
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
                Point(0.09892, 0.00910),
                Point(0.18255, 0.02806),
                Point(0.25496, 0.05915),
                Point(0.31940, 0.10689),
                Point(0.37889, 0.17996),
                Point(0.43703, 0.29649),
                Point(0.50000, 0.50000),
                Point(0.53889, 0.62497),
                Point(0.58863, 0.73209),
                Point(0.64922, 0.82136),
                Point(0.72065, 0.89279),
                Point(0.80292, 0.94637),
                Point(0.89604, 0.98211),
                Point(1, 1),
            ],
            result,
        )
