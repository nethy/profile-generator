from unittest import TestCase

from .contrast_sigmoid import Point, Strength, calculate, calculate_with_hl_protection

_GREY = Point(87 / 255, 119 / 255)
_STRENGTH = Strength(0.5)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calcualate_returns_empty_list_if_sample_size_not_positive(self) -> None:
        self.assertEqual([], calculate(_GREY, _STRENGTH, sample_size=0))
        self.assertEqual([], calculate(_GREY, _STRENGTH, sample_size=-1))

    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(0.000000, 0.000000),
                Point(0.062500, 0.030054),
                Point(0.125000, 0.082296),
                Point(0.187500, 0.163497),
                Point(0.250000, 0.274194),
                Point(0.312500, 0.404754),
                Point(0.375000, 0.538009),
                Point(0.437500, 0.657693),
                Point(0.500000, 0.755014),
                Point(0.562500, 0.828942),
                Point(0.625000, 0.882858),
                Point(0.687500, 0.921397),
                Point(0.750000, 0.948779),
                Point(0.812500, 0.968290),
                Point(0.875000, 0.982310),
                Point(0.937500, 0.992499),
                Point(1.000000, 1.000000),
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
                Point(0.000000, 0.062745),
                Point(0.062500, 0.080242),
                Point(0.125000, 0.115742),
                Point(0.187500, 0.179415),
                Point(0.250000, 0.277287),
                Point(0.312500, 0.402438),
                Point(0.375000, 0.534085),
                Point(0.437500, 0.650094),
                Point(0.500000, 0.739378),
                Point(0.562500, 0.802345),
                Point(0.625000, 0.844720),
                Point(0.687500, 0.872715),
                Point(0.750000, 0.891195),
                Point(0.812500, 0.903507),
                Point(0.875000, 0.911831),
                Point(0.937500, 0.917557),
                Point(1.000000, 0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(0.000000, 0.000000),
                Point(0.062500, 0.030054),
                Point(0.125000, 0.082296),
                Point(0.187500, 0.163497),
                Point(0.250000, 0.274194),
                Point(0.312500, 0.404754),
                Point(0.375000, 0.532860),
                Point(0.437500, 0.632273),
                Point(0.500000, 0.711046),
                Point(0.562500, 0.772905),
                Point(0.625000, 0.822497),
                Point(0.687500, 0.863521),
                Point(0.750000, 0.898439),
                Point(0.812500, 0.928766),
                Point(0.875000, 0.955433),
                Point(0.937500, 0.979037),
                Point(1.000000, 1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(0.000000, 0.062745),
                Point(0.062500, 0.080242),
                Point(0.125000, 0.115742),
                Point(0.187500, 0.179415),
                Point(0.250000, 0.277287),
                Point(0.312500, 0.402438),
                Point(0.375000, 0.527648),
                Point(0.437500, 0.621537),
                Point(0.500000, 0.692332),
                Point(0.562500, 0.745169),
                Point(0.625000, 0.785871),
                Point(0.687500, 0.818600),
                Point(0.750000, 0.845855),
                Point(0.812500, 0.869066),
                Point(0.875000, 0.889079),
                Point(0.937500, 0.906447),
                Point(1.000000, 0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
