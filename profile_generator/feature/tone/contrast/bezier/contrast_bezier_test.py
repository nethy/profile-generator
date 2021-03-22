import unittest

from profile_generator.unit import Point, Strength

from . import contrast_bezier


class ResolveTest(unittest.TestCase):
    def test_calculate_when_strength_is_less_than_1(self) -> None:
        grey = Point(0.3412, 0.46667)
        strength = Strength(0.2)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

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
                Point(0.42205, 0.59280),
                Point(0.50733, 0.70228),
                Point(0.59702, 0.79512),
                Point(0.69114, 0.87131),
                Point(0.78967, 0.93085),
                Point(0.89263, 0.97375),
                Point(1, 1),
            ),
            result,
        )

    def test_calculate_when_strength_is_1(self) -> None:
        grey = Point(0.5, 0.5)
        strength = Strength(1)

        result = contrast_bezier.calculate(grey, strength, (2, 1))

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
                Point(0.51020, 0.61729),
                Point(0.54082, 0.71929),
                Point(0.59184, 0.80600),
                Point(0.66327, 0.87743),
                Point(0.75510, 0.93357),
                Point(0.86735, 0.97443),
                Point(1, 1),
            ),
            result,
        )
