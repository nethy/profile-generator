from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate, calculate_with_hl_protection

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)


class ContrastSigmoid(TestCase):
    def test_calcualate_returns_empty_list_if_sample_size_not_positive(self) -> None:
        self.assertEqual([], calculate(_GREY, _STRENGTH, sample_size=0))
        self.assertEqual([], calculate(_GREY, _STRENGTH, sample_size=-1))

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
            calculate(_GREY, _STRENGTH),
        )

    def test_calculate_linear(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(0.50000, 0.50000),
                Point(1.00000, 1.00000),
            ],
            calculate(Point(0.5, 0.5), Strength(), sample_size=3),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.06275),
                Point(0.06250, 0.07533),
                Point(0.12500, 0.10415),
                Point(0.18750, 0.16214),
                Point(0.25000, 0.26067),
                Point(0.31250, 0.39584),
                Point(0.37500, 0.54184),
                Point(0.43750, 0.66822),
                Point(0.50000, 0.76081),
                Point(0.56250, 0.82204),
                Point(0.62500, 0.86059),
                Point(0.68750, 0.88449),
                Point(0.75000, 0.89937),
                Point(0.81250, 0.90879),
                Point(0.87500, 0.91486),
                Point(0.93750, 0.91887),
                Point(1.00000, 0.92157),
            ],
            calculate(_GREY, _STRENGTH, (16 / 255, 235 / 255)),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.00000),
                Point(0.06250, 0.02338),
                Point(0.12500, 0.06836),
                Point(0.18750, 0.14512),
                Point(0.25000, 0.25824),
                Point(0.31250, 0.39877),
                Point(0.37500, 0.53769),
                Point(0.43750, 0.64193),
                Point(0.50000, 0.72248),
                Point(0.56250, 0.78428),
                Point(0.62500, 0.83300),
                Point(0.68750, 0.87279),
                Point(0.75000, 0.90624),
                Point(0.81250, 0.93488),
                Point(0.87500, 0.95966),
                Point(0.93750, 0.98121),
                Point(1.00000, 1.00000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(0.00000, 0.06275),
                Point(0.06250, 0.07533),
                Point(0.12500, 0.10415),
                Point(0.18750, 0.16214),
                Point(0.25000, 0.26067),
                Point(0.31250, 0.39584),
                Point(0.37500, 0.53285),
                Point(0.43750, 0.63188),
                Point(0.50000, 0.70418),
                Point(0.56250, 0.75667),
                Point(0.62500, 0.79635),
                Point(0.68750, 0.82779),
                Point(0.75000, 0.85353),
                Point(0.81250, 0.87503),
                Point(0.87500, 0.89315),
                Point(0.93750, 0.90851),
                Point(1.00000, 0.92157),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, (16 / 255, 235 / 255)),
        )
