from unittest import TestCase

from .contrast_sigmoid import Point, base_controls, calculate

_NEUTRAL5 = [87.0, 87.0, 87.0]
_GAMMA = 2.5
_EV_COMP = 1.0
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.121569, y=0.048327),
                Point(x=0.219608, y=0.161782),
                Point(x=0.290196, y=0.332905),
                Point(x=0.388235, y=0.635023),
                Point(x=0.517647, y=0.860857),
                Point(x=0.619608, y=0.930587),
                Point(x=0.733333, y=0.967194),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.113725, y=0.046469),
                Point(x=0.207843, y=0.168707),
                Point(x=0.274510, y=0.382426),
                Point(x=0.317647, y=0.576906),
                Point(x=0.352941, y=0.719704),
                Point(x=0.447059, y=0.909961),
                Point(x=0.564706, y=0.969638),
                Point(x=0.690196, y=0.987931),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, offsets=_OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.121569, y=0.095491),
                Point(x=0.227451, y=0.194299),
                Point(x=0.294118, y=0.346738),
                Point(x=0.345098, y=0.506837),
                Point(x=0.388235, y=0.631055),
                Point(x=0.505882, y=0.815286),
                Point(x=0.615686, y=0.874198),
                Point(x=0.725490, y=0.899140),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_base_controls(self) -> None:
        self.assertEqual(
            base_controls(_NEUTRAL5),
            [
                Point(0, 0),
                Point(0.166195, 0.166195),
                Point(0.332391, 0.332391),
                Point(0.666195, 0.666195),
                Point(1, 1),
            ],
        )
