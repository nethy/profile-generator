from unittest import TestCase

from profile_generator.model.sigmoid import HighlighTone

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
                Point(x=0.074510, y=0.021752),
                Point(x=0.200000, y=0.150229),
                Point(x=0.278431, y=0.322164),
                Point(x=0.376471, y=0.575373),
                Point(x=0.533333, y=0.820611),
                Point(x=0.760784, y=0.950711),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.098039, y=0.081605),
                Point(x=0.207843, y=0.177717),
                Point(x=0.282353, y=0.330822),
                Point(x=0.372549, y=0.561847),
                Point(x=0.521569, y=0.780396),
                Point(x=0.733333, y=0.881160),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_NEUTRAL5, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.058824, y=0.027451),
                Point(x=0.160784, y=0.163752),
                Point(x=0.243137, y=0.381585),
                Point(x=0.329412, y=0.633209),
                Point(x=0.458824, y=0.849032),
                Point(x=0.572549, y=0.925761),
                Point(x=0.701961, y=0.965486),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_NEUTRAL5, _GAMMA, ev_comp=_EV_COMP),
        )

    def test_calculate_with_hl_tone_increased(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, HighlighTone.INCREASED),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.066667, y=0.018269),
                Point(x=0.203922, y=0.157123),
                Point(x=0.274510, y=0.312140),
                Point(x=0.384314, y=0.600483),
                Point(x=0.458824, y=0.754723),
                Point(x=0.541176, y=0.863988),
                Point(x=0.749020, y=0.971559),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_hl_tone_decreased(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, HighlighTone.DECREASED),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.066667, y=0.018269),
                Point(x=0.192157, y=0.137030),
                Point(x=0.278431, y=0.322164),
                Point(x=0.364706, y=0.544708),
                Point(x=0.431373, y=0.665092),
                Point(x=0.517647, y=0.770192),
                Point(x=0.737255, y=0.917137),
                Point(x=1.000000, y=1.000000),
            ],
        )
