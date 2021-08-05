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
                Point(x=0.078431, y=0.028485),
                Point(x=0.215686, y=0.173526),
                Point(x=0.298039, y=0.362589),
                Point(x=0.349020, y=0.517825),
                Point(x=0.384314, y=0.613800),
                Point(x=0.517647, y=0.834482),
                Point(x=0.623529, y=0.910927),
                Point(x=0.733333, y=0.952667),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_tone_strength_max(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_MAX),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.109804, y=0.027543),
                Point(x=0.215686, y=0.144417),
                Point(x=0.290196, y=0.331973),
                Point(x=0.392157, y=0.648557),
                Point(x=0.525490, y=0.889651),
                Point(x=0.627451, y=0.955449),
                Point(x=0.741176, y=0.983303),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_tone_strength_min(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_MIN),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.074510, y=0.052340),
                Point(x=0.231373, y=0.233422),
                Point(x=0.301961, y=0.379034),
                Point(x=0.321569, y=0.433022),
                Point(x=0.345098, y=0.504860),
                Point(x=0.380392, y=0.592840),
                Point(x=0.505882, y=0.778399),
                Point(x=0.721569, y=0.919216),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_DEFAULT, offsets=_OFFSETS),
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.219608, y=0.198392),
                Point(x=0.298039, y=0.364948),
                Point(x=0.345098, y=0.505582),
                Point(x=0.380392, y=0.600096),
                Point(x=0.505882, y=0.791593),
                Point(x=0.611765, y=0.854382),
                Point(x=0.725490, y=0.886905),
                Point(x=1.000000, y=0.921569),
            ],
        )

    def test_calculate_with_exposure_compensation(self) -> None:
        self.assertEqual(
            calculate(_NEUTRAL5, _GAMMA, _HL_TONE_DEFAULT, ev_comp=_EV_COMP),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.105882, y=0.047933),
                Point(x=0.196078, y=0.174244),
                Point(x=0.278431, y=0.424033),
                Point(x=0.317647, y=0.580351),
                Point(x=0.352941, y=0.715274),
                Point(x=0.392157, y=0.813514),
                Point(x=0.443137, y=0.886200),
                Point(x=0.564706, y=0.954821),
                Point(x=0.690196, y=0.978958),
                Point(x=1.000000, y=1.000000),
            ],
        )
