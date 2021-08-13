from unittest import TestCase

from .contrast_sigmoid import Point, base_controls, calculate

_NEUTRAL5 = 87.0
_GAMMA = 2.5
_EV_COMP = 1.0
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.121569, y=0.048743),
                Point(x=0.219608, y=0.163231),
                Point(x=0.290196, y=0.333677),
                Point(x=0.388235, y=0.631200),
                Point(x=0.517647, y=0.856099),
                Point(x=0.619608, y=0.927157),
                Point(x=0.733333, y=0.965119),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.121569, y=0.095687),
                Point(x=0.227451, y=0.195312),
                Point(x=0.294118, y=0.347183),
                Point(x=0.341176, y=0.492894),
                Point(x=0.388235, y=0.627670),
                Point(x=0.505882, y=0.811729),
                Point(x=0.611765, y=0.870539),
                Point(x=0.725490, y=0.897767),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_base_controls(self) -> None:
        self.assertEqual(
            base_controls(_NEUTRAL5),
            [
                Point(0, 0),
                Point(0.166371, 0.166371),
                Point(0.332741, 0.332741),
                Point(0.666371, 0.666371),
                Point(1, 1),
            ],
        )

    def test_base_controls_ev_comp(self) -> None:
        self.assertEqual(
            base_controls(_NEUTRAL5, ev_comp=_EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.103581),
                Point(x=0.160784, y=0.248509),
                Point(x=0.431373, y=0.566987),
                Point(x=0.784314, y=0.862571),
                Point(x=1.000000, y=1.000000),
            ],
        )
