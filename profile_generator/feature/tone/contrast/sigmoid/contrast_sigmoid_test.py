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
                Point(x=0.121569, y=0.049548),
                Point(x=0.219608, y=0.164097),
                Point(x=0.290196, y=0.333897),
                Point(x=0.388235, y=0.631553),
                Point(x=0.517647, y=0.857520),
                Point(x=0.619608, y=0.928551),
                Point(x=0.733333, y=0.966137),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.121569, y=0.096259),
                Point(x=0.227451, y=0.196005),
                Point(x=0.294118, y=0.347363),
                Point(x=0.345098, y=0.505142),
                Point(x=0.388235, y=0.628006),
                Point(x=0.505882, y=0.812813),
                Point(x=0.611765, y=0.871539),
                Point(x=0.725490, y=0.898469),
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

    def test_base_controls_ev_corr(self) -> None:
        self.assertEqual(
            base_controls(_NEUTRAL5, 1),
            [
                Point(0, 0),
                Point(0.235478, 0.332741),
                Point(0.667259, 0.764522),
                Point(1, 1),
            ],
        )

    def test_base_controls_ev_comp(self) -> None:
        self.assertEqual(
            base_controls(_NEUTRAL5, ev_comp=1),
            [
                Point(0, 0),
                Point(0.332741, 0.462572),
                Point(0.537428, 0.667259),
                Point(1, 1),
            ],
        )
