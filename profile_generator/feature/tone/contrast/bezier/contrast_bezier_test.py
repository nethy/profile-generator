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
                Point(0.04348, 0.02033),
                Point(0.07560, 0.04574),
                Point(0.10537, 0.07873),
                Point(0.13809, 0.12348),
                Point(0.17943, 0.18777),
                Point(0.23923, 0.28809),
                Point(0.34118, 0.46667),
                Point(0.41859, 0.59102),
                Point(0.50157, 0.69933),
                Point(0.59012, 0.79157),
                Point(0.68423, 0.86776),
                Point(0.78392, 0.92790),
                Point(0.88918, 0.97198),
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
                Point(0.13846, 0.01695),
                Point(0.22092, 0.04188),
                Point(0.27934, 0.07627),
                Point(0.32729, 0.12421),
                Point(0.37309, 0.19405),
                Point(0.42535, 0.30383),
                Point(0.50000, 0.50000),
                Point(0.54975, 0.62206),
                Point(0.60673, 0.72724),
                Point(0.67093, 0.81554),
                Point(0.74236, 0.88697),
                Point(0.82101, 0.94152),
                Point(0.90689, 0.97920),
                Point(1, 1),
            ],
            result,
        )
