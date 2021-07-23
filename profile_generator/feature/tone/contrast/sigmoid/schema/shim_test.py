from unittest import TestCase

from profile_generator.model.sigmoid import HighlighTone

from .shim import Point, get_parameters, marshal_curve

_DEFAULT_GAMMA = 1.0
_DEFAULT_NEUTRAL5 = [90.0, 90.0, 90.0]
_DEFAULT_EV_COMP = 0.0
_DEFAULT_HL_TONE = HighlighTone.NORMAL


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        netrual5, gamma, hl_tone, ev_comp, offsets = get_parameters({})

        self.assertEqual(netrual5, _DEFAULT_NEUTRAL5)
        self.assertEqual(gamma, _DEFAULT_GAMMA)
        self.assertEqual(hl_tone, _DEFAULT_HL_TONE)
        self.assertEqual(ev_comp, _DEFAULT_EV_COMP)
        self.assertEqual(offsets, (0, 1))

    def test_get_parameters_neutral5(self) -> None:
        neutral5, _, _, _, _ = get_parameters({"neutral5": [87, 87, 87]})
        self.assertEqual(neutral5, [87, 87, 87])

    def test_get_parameters_gamma(self) -> None:
        _, gamma, _, _, _ = get_parameters({"gamma": 2.0})
        self.assertEqual(gamma, 2.0)

    def test_get_parameters_hl_tone(self) -> None:
        _, _, hl_tone, _, _ = get_parameters({"highlight_tone": "NORMAL"})
        self.assertEqual(hl_tone, HighlighTone.NORMAL)

        _, _, hl_tone, _, _ = get_parameters({"highlight_tone": "INCREASED"})
        self.assertEqual(hl_tone, HighlighTone.INCREASED)

        _, _, hl_tone, _, _ = get_parameters({"highlight_tone": "DECREASED"})
        self.assertEqual(hl_tone, HighlighTone.DECREASED)

    def test_get_parameters_exposure_compensation(self) -> None:
        _, _, _, ev_comp, _ = get_parameters({"exposure_compensation": -1})
        self.assertEqual(ev_comp, -1)

    def test_get_parameters_matte_effect(self) -> None:
        _, _, _, _, offsets = get_parameters({"matte_effect": True})
        self.assertEqual(offsets, (16 / 255, 1.0))

    def test_marshal_curve(self) -> None:
        self.assertEqual({"Curve": "0;"}, marshal_curve([]))
        self.assertEqual(
            {"Curve": "1;0.000000;0.000000;1.000000;1.000000;"},
            marshal_curve([Point(0, 0), Point(1, 1)]),
        )
