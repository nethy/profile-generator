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
                Point(x=0.041667, y=0.017976),
                Point(x=0.083333, y=0.044604),
                Point(x=0.125000, y=0.082296),
                Point(x=0.166667, y=0.132989),
                Point(x=0.208333, y=0.197375),
                Point(x=0.250000, y=0.274194),
                Point(x=0.291667, y=0.360015),
                Point(x=0.333333, y=0.449783),
                Point(x=0.375000, y=0.538010),
                Point(x=0.416667, y=0.620031),
                Point(x=0.458333, y=0.692803),
                Point(x=0.500000, y=0.755014),
                Point(x=0.541667, y=0.806740),
                Point(x=0.583333, y=0.848912),
                Point(x=0.625000, y=0.882858),
                Point(x=0.666667, y=0.909981),
                Point(x=0.708333, y=0.931581),
                Point(x=0.750000, y=0.948779),
                Point(x=0.791667, y=0.962497),
                Point(x=0.833333, y=0.973479),
                Point(x=0.875000, y=0.982310),
                Point(x=0.916667, y=0.989449),
                Point(x=0.958333, y=0.995253),
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
                Point(x=0.041667, y=0.072886),
                Point(x=0.083333, y=0.089577),
                Point(x=0.125000, y=0.115742),
                Point(x=0.166667, y=0.154501),
                Point(x=0.208333, y=0.208244),
                Point(x=0.250000, y=0.277287),
                Point(x=0.291667, y=0.358783),
                Point(x=0.333333, y=0.446824),
                Point(x=0.375000, y=0.534085),
                Point(x=0.416667, y=0.614129),
                Point(x=0.458333, y=0.682988),
                Point(x=0.500000, y=0.739378),
                Point(x=0.541667, y=0.783969),
                Point(x=0.583333, y=0.818433),
                Point(x=0.625000, y=0.844720),
                Point(x=0.666667, y=0.864648),
                Point(x=0.708333, y=0.879738),
                Point(x=0.750000, y=0.891195),
                Point(x=0.791667, y=0.899934),
                Point(x=0.833333, y=0.906643),
                Point(x=0.875000, y=0.911831),
                Point(x=0.916667, y=0.915875),
                Point(x=0.958333, y=0.919052),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.041667, y=0.017976),
                Point(x=0.083333, y=0.044604),
                Point(x=0.125000, y=0.082296),
                Point(x=0.166667, y=0.132989),
                Point(x=0.208333, y=0.197375),
                Point(x=0.250000, y=0.274194),
                Point(x=0.291667, y=0.360015),
                Point(x=0.333333, y=0.449783),
                Point(x=0.375000, y=0.532861),
                Point(x=0.416667, y=0.601519),
                Point(x=0.458333, y=0.660695),
                Point(x=0.500000, y=0.711047),
                Point(x=0.541667, y=0.753868),
                Point(x=0.583333, y=0.790590),
                Point(x=0.625000, y=0.822497),
                Point(x=0.666667, y=0.850624),
                Point(x=0.708333, y=0.875749),
                Point(x=0.750000, y=0.898439),
                Point(x=0.791667, y=0.919101),
                Point(x=0.833333, y=0.938027),
                Point(x=0.875000, y=0.955433),
                Point(x=0.916667, y=0.971481),
                Point(x=0.958333, y=0.986301),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.041667, y=0.072886),
                Point(x=0.083333, y=0.089577),
                Point(x=0.125000, y=0.115742),
                Point(x=0.166667, y=0.154501),
                Point(x=0.208333, y=0.208244),
                Point(x=0.250000, y=0.277287),
                Point(x=0.291667, y=0.358783),
                Point(x=0.333333, y=0.446824),
                Point(x=0.375000, y=0.527648),
                Point(x=0.416667, y=0.592940),
                Point(x=0.458333, y=0.647514),
                Point(x=0.500000, y=0.692332),
                Point(x=0.541667, y=0.729166),
                Point(x=0.583333, y=0.759839),
                Point(x=0.625000, y=0.785871),
                Point(x=0.666667, y=0.808394),
                Point(x=0.708333, y=0.828206),
                Point(x=0.750000, y=0.845855),
                Point(x=0.791667, y=0.861718),
                Point(x=0.833333, y=0.876061),
                Point(x=0.875000, y=0.889079),
                Point(x=0.916667, y=0.900925),
                Point(x=0.958333, y=0.911720),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
