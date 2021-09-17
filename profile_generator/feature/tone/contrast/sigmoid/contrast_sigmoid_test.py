from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_GAMMA = 2.5
_EV_COMP = 1.0
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.121569, y=0.052725),
                Point(x=0.223529, y=0.166663),
                Point(x=0.298039, y=0.336033),
                Point(x=0.352941, y=0.502333),
                Point(x=0.392157, y=0.609967),
                Point(x=0.525490, y=0.827827),
                Point(x=0.627451, y=0.902286),
                Point(x=0.737255, y=0.946812),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_offests(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.125490, y=0.100560),
                Point(x=0.231373, y=0.197441),
                Point(x=0.301961, y=0.348901),
                Point(x=0.352941, y=0.501993),
                Point(x=0.388235, y=0.596283),
                Point(x=0.513725, y=0.783858),
                Point(x=0.619608, y=0.847466),
                Point(x=0.729412, y=0.881663),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_calculate_highlight_protection(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, highlight_protection=True),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.117647, y=0.050080),
                Point(x=0.219608, y=0.160118),
                Point(x=0.294118, y=0.325033),
                Point(x=0.349020, y=0.490156),
                Point(x=0.384314, y=0.582787),
                Point(x=0.439216, y=0.689532),
                Point(x=0.521569, y=0.795140),
                Point(x=0.654902, y=0.893154),
                Point(x=0.788235, y=0.948018),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_ev_comp(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, ev_comp=_EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.082353, y=0.052742),
                Point(x=0.149020, y=0.157557),
                Point(x=0.200000, y=0.312714),
                Point(x=0.247059, y=0.504192),
                Point(x=0.278431, y=0.616555),
                Point(x=0.400000, y=0.844418),
                Point(x=0.529412, y=0.926246),
                Point(x=0.662745, y=0.962730),
                Point(x=1.000000, y=1.000000),
            ],
        )
