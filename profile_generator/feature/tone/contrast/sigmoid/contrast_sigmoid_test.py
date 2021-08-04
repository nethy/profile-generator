from unittest import TestCase

from profile_generator.unit.strength import Strength

from .contrast_sigmoid import Point, calculate

_NEUTRAL5 = [87.0, 87.0, 87.0]
_GAMMA = 2.5
_EV_COMP = 1.0
_HL_TONE_DEFAULT = Strength()
_HL_TONE_MAX = Strength(1)
_HL_TONE_MIN = Strength(-1)
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_DEFAULT),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.207843, y=0.167438),
                Point(x=0.278431, y=0.319461),
                Point(x=0.341176, y=0.490315),
                Point(x=0.380392, y=0.587141),
                Point(x=0.525490, y=0.812182),
                Point(x=0.639216, y=0.896688),
                Point(x=0.752941, y=0.945502),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_hl_tone_max(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_MAX),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.211765, y=0.174213),
                Point(x=0.286275, y=0.339845),
                Point(x=0.388235, y=0.613048),
                Point(x=0.529412, y=0.844560),
                Point(x=0.631373, y=0.917964),
                Point(x=0.741176, y=0.959131),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_hl_tone_min(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_MIN),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.203922, y=0.160860),
                Point(x=0.278431, y=0.319461),
                Point(x=0.368627, y=0.555618),
                Point(x=0.431373, y=0.670231),
                Point(x=0.517647, y=0.776996),
                Point(x=0.737255, y=0.922479),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_DEFAULT, offsets=_OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.117647, y=0.102458),
                Point(x=0.215686, y=0.197091),
                Point(x=0.286275, y=0.341184),
                Point(x=0.341176, y=0.490260),
                Point(x=0.376471, y=0.576079),
                Point(x=0.513725, y=0.772544),
                Point(x=0.619608, y=0.838966),
                Point(x=0.729412, y=0.877173),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_DEFAULT, ev_comp=_EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.043137, y=0.024917),
                Point(x=0.176471, y=0.192240),
                Point(x=0.254902, y=0.398779),
                Point(x=0.341176, y=0.664844),
                Point(x=0.454902, y=0.855898),
                Point(x=0.572549, y=0.931484),
                Point(x=0.698039, y=0.967152),
                Point(x=1.000000, y=1.000000),
            ],
        )
