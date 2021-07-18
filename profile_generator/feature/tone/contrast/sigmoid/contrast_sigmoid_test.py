from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_NEUTRAL5 = [87.0, 87.0, 87.0]
_GAMMA = 2.5
_EV_COMP = 1.0
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.074510, y=0.021922),
                Point(x=0.203922, y=0.159629),
                Point(x=0.384314, y=0.597994),
                Point(x=0.458824, y=0.750126),
                Point(x=0.541176, y=0.859515),
                Point(x=0.749020, y=0.970121),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.098039, y=0.081819),
                Point(x=0.211765, y=0.186026),
                Point(x=0.286275, y=0.342585),
                Point(x=0.388235, y=0.603215),
                Point(x=0.529412, y=0.819798),
                Point(x=0.627451, y=0.877408),
                Point(x=0.741176, y=0.904906),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_NEUTRAL5, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.062745, y=0.029597),
                Point(x=0.160784, y=0.162865),
                Point(x=0.321569, y=0.612660),
                Point(x=0.392157, y=0.770739),
                Point(x=0.470588, y=0.877740),
                Point(x=0.580392, y=0.949461),
                Point(x=0.709804, y=0.981897),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA, _EV_COMP),
        )
