from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY = Point(87 / 255, 119 / 255)
_GAMMA = 2.5
_HL_PROTECTION = 2.5
_OFFSETS = (16 / 255, 235 / 255)


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.152941, y=0.000161),
                Point(x=0.219608, y=0.004496),
                Point(x=0.247059, y=0.015888),
                Point(x=0.274510, y=0.051951),
                Point(x=0.317647, y=0.253303),
                Point(x=0.352941, y=0.581400),
                Point(x=0.376471, y=0.773843),
                Point(x=0.439216, y=0.970613),
                Point(x=0.486275, y=0.993807),
                Point(x=0.537255, y=0.998754),
                Point(x=0.678431, y=0.999976),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA),
        )

    def test_calculate_with_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.156863, y=0.062785),
                Point(x=0.223529, y=0.064668),
                Point(x=0.254902, y=0.073105),
                Point(x=0.282353, y=0.103973),
                Point(x=0.321569, y=0.284049),
                Point(x=0.349020, y=0.541141),
                Point(x=0.372549, y=0.736706),
                Point(x=0.427451, y=0.899759),
                Point(x=0.478431, y=0.918659),
                Point(x=0.525490, y=0.921069),
                Point(x=0.670588, y=0.921565),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, offsets=_OFFSETS),
        )

    def test_calculate_with_hl_protection(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.152941, y=0.000161),
                Point(x=0.219608, y=0.004496),
                Point(x=0.247059, y=0.015888),
                Point(x=0.274510, y=0.051951),
                Point(x=0.317647, y=0.253303),
                Point(x=0.352941, y=0.579881),
                Point(x=0.376471, y=0.762494),
                Point(x=0.435294, y=0.934368),
                Point(x=0.486275, y=0.963086),
                Point(x=0.533333, y=0.974579),
                Point(x=0.678431, y=0.991912),
                Point(x=1.000000, y=1.000000),
            ],
            calculate(_GREY, _GAMMA, _HL_PROTECTION),
        )

    def test_calculate_with_hl_protection_and_offests(self) -> None:
        self.assertEqual(
            [
                Point(x=0.000000, y=0.062745),
                Point(x=0.156863, y=0.062785),
                Point(x=0.223529, y=0.064668),
                Point(x=0.250980, y=0.071184),
                Point(x=0.278431, y=0.096826),
                Point(x=0.321569, y=0.284049),
                Point(x=0.349020, y=0.540453),
                Point(x=0.372549, y=0.727782),
                Point(x=0.400000, y=0.836389),
                Point(x=0.427451, y=0.875869),
                Point(x=0.474510, y=0.897123),
                Point(x=0.525490, y=0.906632),
                Point(x=0.670588, y=0.917924),
                Point(x=1.000000, y=0.921569),
            ],
            calculate(_GREY, _GAMMA, _HL_PROTECTION, _OFFSETS),
        )
