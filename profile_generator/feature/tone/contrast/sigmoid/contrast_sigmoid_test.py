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
                Point(x=0.062500, y=0.023378),
                Point(x=0.125000, y=0.068358),
                Point(x=0.187500, y=0.145127),
                Point(x=0.250000, y=0.258245),
                Point(x=0.312500, y=0.398776),
                Point(x=0.375000, y=0.545012),
                Point(x=0.437500, y=0.674784),
                Point(x=0.500000, y=0.776665),
                Point(x=0.562500, y=0.850446),
                Point(x=0.625000, y=0.901522),
                Point(x=0.687500, y=0.936202),
                Point(x=0.750000, y=0.959682),
                Point(x=0.812500, y=0.975689),
                Point(x=0.875000, y=0.986739),
                Point(x=0.937500, y=0.994483),
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
                Point(x=0.062500, y=0.075328),
                Point(x=0.125000, y=0.104147),
                Point(x=0.187500, y=0.162138),
                Point(x=0.250000, y=0.260674),
                Point(x=0.312500, y=0.395838),
                Point(x=0.375000, y=0.541841),
                Point(x=0.437500, y=0.668223),
                Point(x=0.500000, y=0.760807),
                Point(x=0.562500, y=0.822043),
                Point(x=0.625000, y=0.860588),
                Point(x=0.687500, y=0.884486),
                Point(x=0.750000, y=0.899372),
                Point(x=0.812500, y=0.908787),
                Point(x=0.875000, y=0.914861),
                Point(x=0.937500, y=0.918867),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _STRENGTH, _OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062500, y=0.023378),
                Point(x=0.125000, y=0.068358),
                Point(x=0.187500, y=0.145127),
                Point(x=0.250000, y=0.258245),
                Point(x=0.312500, y=0.398776),
                Point(x=0.375000, y=0.537690),
                Point(x=0.437500, y=0.641934),
                Point(x=0.500000, y=0.722483),
                Point(x=0.562500, y=0.784285),
                Point(x=0.625000, y=0.833000),
                Point(x=0.687500, y=0.872788),
                Point(x=0.750000, y=0.906237),
                Point(x=0.812500, y=0.934880),
                Point(x=0.875000, y=0.959660),
                Point(x=0.937500, y=0.981210),
                Point(x=1.000000, y=1.000000),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.062500, y=0.075328),
                Point(x=0.125000, y=0.104147),
                Point(x=0.187500, y=0.162138),
                Point(x=0.250000, y=0.260674),
                Point(x=0.312500, y=0.395838),
                Point(x=0.375000, y=0.532851),
                Point(x=0.437500, y=0.631877),
                Point(x=0.500000, y=0.704182),
                Point(x=0.562500, y=0.756669),
                Point(x=0.625000, y=0.796352),
                Point(x=0.687500, y=0.827786),
                Point(x=0.750000, y=0.853532),
                Point(x=0.812500, y=0.875026),
                Point(x=0.875000, y=0.893149),
                Point(x=0.937500, y=0.908509),
                Point(x=1.000000, y=0.921569),
            ],
            calculate_with_hl_protection(_GREY, _STRENGTH, _OFFSETS),
        )
