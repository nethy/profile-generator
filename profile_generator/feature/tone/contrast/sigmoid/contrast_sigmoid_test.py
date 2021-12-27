from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_SLOPE = 2.5
_BRIGHTNESS = 1.0


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.111111, y=0.021658),
                Point(x=0.166667, y=0.053889),
                Point(x=0.214286, y=0.111041),
                Point(x=0.238095, y=0.159987),
                Point(x=0.261905, y=0.228554),
                Point(x=0.277778, y=0.276165),
                Point(x=0.349206, y=0.490412),
                Point(x=0.388889, y=0.606446),
                Point(x=0.452381, y=0.731688),
                Point(x=0.515873, y=0.808581),
                Point(x=0.619048, y=0.885339),
                Point(x=0.722222, y=0.932508),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.079365, y=0.021315),
                Point(x=0.119048, y=0.052794),
                Point(x=0.150794, y=0.103154),
                Point(x=0.174603, y=0.171352),
                Point(x=0.182540, y=0.203388),
                Point(x=0.198413, y=0.269510),
                Point(x=0.253968, y=0.500938),
                Point(x=0.285714, y=0.626197),
                Point(x=0.309524, y=0.694778),
                Point(x=0.333333, y=0.746927),
                Point(x=0.396825, y=0.835387),
                Point(x=0.523810, y=0.916812),
                Point(x=0.658730, y=0.956873),
                Point(x=1.000000, y=1.000000),
            ],
        )
