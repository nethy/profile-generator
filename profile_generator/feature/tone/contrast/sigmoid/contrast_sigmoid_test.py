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
                Point(x=0.113725, y=0.035484),
                Point(x=0.219608, y=0.150795),
                Point(x=0.294118, y=0.323946),
                Point(x=0.388235, y=0.600681),
                Point(x=0.529412, y=0.839004),
                Point(x=0.635294, y=0.914119),
                Point(x=0.741176, y=0.953703),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_offests(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.117647, y=0.084464),
                Point(x=0.223529, y=0.174759),
                Point(x=0.298039, y=0.336841),
                Point(x=0.352941, y=0.502008),
                Point(x=0.388235, y=0.597061),
                Point(x=0.517647, y=0.795304),
                Point(x=0.619608, y=0.855529),
                Point(x=0.733333, y=0.888011),
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
                Point(x=0.145098, y=0.138597),
                Point(x=0.200000, y=0.311325),
                Point(x=0.247059, y=0.504203),
                Point(x=0.278431, y=0.617290),
                Point(x=0.403922, y=0.856039),
                Point(x=0.541176, y=0.937468),
                Point(x=0.666667, y=0.967837),
                Point(x=1.000000, y=1.000000),
            ],
        )
