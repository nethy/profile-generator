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
                Point(x=0.078431, y=0.029364),
                Point(x=0.200000, y=0.165243),
                Point(x=0.278431, y=0.331873),
                Point(x=0.388235, y=0.599825),
                Point(x=0.545098, y=0.850898),
                Point(x=0.647059, y=0.925872),
                Point(x=0.768627, y=0.969580),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.207843, y=0.190601),
                Point(x=0.286275, y=0.348999),
                Point(x=0.388235, y=0.595937),
                Point(x=0.533333, y=0.812640),
                Point(x=0.631373, y=0.871773),
                Point(x=0.745098, y=0.901755),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_NEUTRAL5, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.066667, y=0.035833),
                Point(x=0.160784, y=0.170723),
                Point(x=0.321569, y=0.613199),
                Point(x=0.392157, y=0.769165),
                Point(x=0.470588, y=0.876280),
                Point(x=0.580392, y=0.948718),
                Point(x=0.709804, y=0.981536),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA, _EV_COMP),
        )
