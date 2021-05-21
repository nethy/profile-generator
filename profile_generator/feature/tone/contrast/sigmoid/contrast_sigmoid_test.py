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
                Point(x=0.000000, y=0.000000),
                Point(x=0.062500, y=0.030054),
                Point(x=0.125000, y=0.082296),
                Point(x=0.187500, y=0.163497),
                Point(x=0.250000, y=0.274193),
                Point(x=0.312500, y=0.404754),
                Point(x=0.375000, y=0.538009),
                Point(x=0.437500, y=0.657693),
                Point(x=0.500000, y=0.755014),
                Point(x=0.562500, y=0.828942),
                Point(x=0.625000, y=0.882858),
                Point(x=0.687500, y=0.921397),
                Point(x=0.750000, y=0.948779),
                Point(x=0.812500, y=0.968290),
                Point(x=0.875000, y=0.982310),
                Point(x=0.937500, y=0.992499),
                Point(x=1.000000, y=1.000000),
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
                Point(x=0.000000, y=0.062745),
                Point(x=0.062500, y=0.080242),
                Point(x=0.125000, y=0.115742),
                Point(x=0.187500, y=0.179415),
                Point(x=0.250000, y=0.277287),
                Point(x=0.312500, y=0.402438),
                Point(x=0.375000, y=0.534085),
                Point(x=0.437500, y=0.650094),
                Point(x=0.500000, y=0.739378),
                Point(x=0.562500, y=0.802345),
                Point(x=0.625000, y=0.844720),
                Point(x=0.687500, y=0.872715),
                Point(x=0.750000, y=0.891195),
                Point(x=0.812500, y=0.903507),
                Point(x=0.875000, y=0.911831),
                Point(x=0.937500, y=0.917557),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062500, y=0.030054),
                Point(x=0.125000, y=0.082296),
                Point(x=0.187500, y=0.163497),
                Point(x=0.250000, y=0.274193),
                Point(x=0.312500, y=0.404754),
                Point(x=0.375000, y=0.532860),
                Point(x=0.437500, y=0.632273),
                Point(x=0.500000, y=0.711046),
                Point(x=0.562500, y=0.772905),
                Point(x=0.625000, y=0.822497),
                Point(x=0.687500, y=0.863521),
                Point(x=0.750000, y=0.898439),
                Point(x=0.812500, y=0.928766),
                Point(x=0.875000, y=0.955433),
                Point(x=0.937500, y=0.979037),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.062500, y=0.080242),
                Point(x=0.125000, y=0.115742),
                Point(x=0.187500, y=0.179415),
                Point(x=0.250000, y=0.277287),
                Point(x=0.312500, y=0.402438),
                Point(x=0.375000, y=0.527648),
                Point(x=0.437500, y=0.621537),
                Point(x=0.500000, y=0.692332),
                Point(x=0.562500, y=0.745169),
                Point(x=0.625000, y=0.785871),
                Point(x=0.687500, y=0.818600),
                Point(x=0.750000, y=0.845855),
                Point(x=0.812500, y=0.869066),
                Point(x=0.875000, y=0.889079),
                Point(x=0.937500, y=0.906447),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
