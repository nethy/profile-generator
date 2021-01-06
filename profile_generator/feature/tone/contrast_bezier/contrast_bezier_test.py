import unittest

from unit import Point, Strength

from . import contrast_bezier


class ResolveTest(unittest.TestCase):
    def test_calculate_when_strength_is_less_than_1(self) -> None:
        grey = Point(0.3412, 0.46667)
        strength = Strength(0.2)

        result = contrast_bezier.calculate(grey, strength)

        self.assertSequenceEqual(
            (
                Point(0, 0),
                Point(0.03966, 0.01999),
                Point(0.06998, 0.04524),
                Point(0.09900, 0.07816),
                Point(0.13172, 0.12291),
                Point(0.17382, 0.18727),
                Point(0.23543, 0.28775),
                Point(0.34120, 0.46667),
                Point(0.42262, 0.59376),
                Point(0.50826, 0.70388),
                Point(0.59815, 0.79704),
                Point(0.69226, 0.87323),
                Point(0.79061, 0.93245),
                Point(0.89319, 0.97471),
                Point(1, 1),
            ),
            result,
        )

    def test_calculate_when_strength_is_1(self) -> None:
        grey = Point(0.5, 0.5)
        strength = Strength(1)

        result = contrast_bezier.calculate(grey, strength)

        self.assertSequenceEqual(
            (
                Point(0, 0),
                Point(0.20492, 0.02054),
                Point(0.31884, 0.04717),
                Point(0.39041, 0.08227),
                Point(0.43836, 0.13022),
                Point(0.47101, 0.19935),
                Point(0.49180, 0.30743),
                Point(0.50000, 0.50000),
                Point(0.51020, 0.61825),
                Point(0.54082, 0.72089),
                Point(0.59184, 0.80792),
                Point(0.66327, 0.87935),
                Point(0.75510, 0.93517),
                Point(0.86735, 0.97539),
                Point(1, 1),
            ),
            result,
        )
