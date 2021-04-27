from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)


class ContrastSigmoid(TestCase):
    def test_calcualate_returns_empty_list_if_sample_size_not_positive(self) -> None:
        self.assertEqual([], calculate(_GREY, _STRENGTH, 0))
        self.assertEqual([], calculate(_GREY, _STRENGTH, -1))

    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(0.06250, 0.02338),
                Point(0.12500, 0.06836),
                Point(0.18750, 0.14512),
                Point(0.25000, 0.25824),
                Point(0.31250, 0.39877),
                Point(0.37500, 0.54501),
                Point(0.43750, 0.67478),
                Point(0.50000, 0.77666),
                Point(0.56250, 0.85044),
                Point(0.62500, 0.90152),
                Point(0.68750, 0.93620),
                Point(0.75000, 0.95968),
                Point(0.81250, 0.97569),
                Point(0.87500, 0.98674),
                Point(0.93750, 0.99448),
                Point(1.00000, 1.00000),
            ],
            calculate(_GREY, _STRENGTH, 17),
        )

    def test_calculate_linear(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(0.50000, 0.50000),
                Point(1.00000, 1.00000),
            ],
            calculate(Point(0.5, 0.5), Strength(), 3),
        )
