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
                Point(x=0.062500, y=0.023211),
                Point(x=0.125000, y=0.067773),
                Point(x=0.187500, y=0.143790),
                Point(x=0.250000, y=0.255946),
                Point(x=0.312500, y=0.395700),
                Point(x=0.375000, y=0.541719),
                Point(x=0.437500, y=0.671846),
                Point(x=0.500000, y=0.774374),
                Point(x=0.562500, y=0.848817),
                Point(x=0.625000, y=0.900435),
                Point(x=0.687500, y=0.935510),
                Point(x=0.750000, y=0.959261),
                Point(x=0.812500, y=0.975449),
                Point(x=0.875000, y=0.986615),
                Point(x=0.937500, y=0.994435),
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
                Point(x=0.062500, y=0.075234),
                Point(x=0.125000, y=0.103757),
                Point(x=0.187500, y=0.161093),
                Point(x=0.250000, y=0.258631),
                Point(x=0.312500, y=0.392897),
                Point(x=0.375000, y=0.538676),
                Point(x=0.437500, y=0.665541),
                Point(x=0.500000, y=0.758884),
                Point(x=0.562500, y=0.820800),
                Point(x=0.625000, y=0.859832),
                Point(x=0.687500, y=0.884045),
                Point(x=0.750000, y=0.899124),
                Point(x=0.812500, y=0.908654),
                Point(x=0.875000, y=0.914797),
                Point(x=0.937500, y=0.918843),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062500, y=0.023211),
                Point(x=0.125000, y=0.067773),
                Point(x=0.187500, y=0.143790),
                Point(x=0.250000, y=0.255946),
                Point(x=0.312500, y=0.395700),
                Point(x=0.375000, y=0.535564),
                Point(x=0.437500, y=0.641803),
                Point(x=0.500000, y=0.723502),
                Point(x=0.562500, y=0.785626),
                Point(x=0.625000, y=0.834148),
                Point(x=0.687500, y=0.873542),
                Point(x=0.750000, y=0.906600),
                Point(x=0.812500, y=0.934955),
                Point(x=0.875000, y=0.959585),
                Point(x=0.937500, y=0.981116),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.062500, y=0.075234),
                Point(x=0.125000, y=0.103757),
                Point(x=0.187500, y=0.161093),
                Point(x=0.250000, y=0.258631),
                Point(x=0.312500, y=0.392897),
                Point(x=0.375000, y=0.531034),
                Point(x=0.437500, y=0.632220),
                Point(x=0.500000, y=0.705615),
                Point(x=0.562500, y=0.758257),
                Point(x=0.625000, y=0.797608),
                Point(x=0.687500, y=0.828581),
                Point(x=0.750000, y=0.853924),
                Point(x=0.812500, y=0.875141),
                Point(x=0.875000, y=0.893120),
                Point(x=0.937500, y=0.908450),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
