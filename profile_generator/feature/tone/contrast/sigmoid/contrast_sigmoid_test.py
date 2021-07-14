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
                Point(x=0.082353, y=0.033165),
                Point(x=0.203922, y=0.173103),
                Point(x=0.278431, y=0.332026),
                Point(x=0.388235, y=0.599889),
                Point(x=0.545098, y=0.850464),
                Point(x=0.647059, y=0.924895),
                Point(x=0.768627, y=0.968548),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.207843, y=0.191366),
                Point(x=0.286275, y=0.349099),
                Point(x=0.388235, y=0.596000),
                Point(x=0.533333, y=0.812254),
                Point(x=0.631373, y=0.870917),
                Point(x=0.745098, y=0.900873),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_NEUTRAL5, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.058824, y=0.035464),
                Point(x=0.164706, y=0.185092),
                Point(x=0.235294, y=0.365054),
                Point(x=0.325490, y=0.623366),
                Point(x=0.466667, y=0.869035),
                Point(x=0.580392, y=0.943921),
                Point(x=0.709804, y=0.977919),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA, _EV_COMP),
        )
