from unittest import TestCase

from .contrast_sigmoid import Point, base_controls, calculate

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
                Point(x=0.125490, y=0.049103),
                Point(x=0.227451, y=0.166559),
                Point(x=0.298039, y=0.334378),
                Point(x=0.400000, y=0.637506),
                Point(x=0.529412, y=0.857396),
                Point(x=0.631373, y=0.927858),
                Point(x=0.737255, y=0.963935),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.125490, y=0.095897),
                Point(x=0.231373, y=0.191662),
                Point(x=0.301961, y=0.347560),
                Point(x=0.396078, y=0.624075),
                Point(x=0.513725, y=0.809615),
                Point(x=0.619608, y=0.869725),
                Point(x=0.729412, y=0.896954),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_base_controls(self) -> None:
        self.assertEqual(
            base_controls(_GREY18),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.170588, y=0.170588),
                Point(x=0.341176, y=0.341176),
                Point(x=0.670588, y=0.670588),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_base_controls_ev_comp(self) -> None:
        self.assertEqual(
            base_controls(_GREY18, _EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.104276),
                Point(x=0.160784, y=0.249906),
                Point(x=0.431373, y=0.568819),
                Point(x=0.784314, y=0.863453),
                Point(x=1.000000, y=1.000000),
            ],
        )
