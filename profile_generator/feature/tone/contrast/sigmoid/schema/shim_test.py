from unittest import TestCase

from .shim import Point, get_parameters, marshal_curve

_DEFAULT_GAMMA = 1.0
_DEFAULT_GREY18 = 90.0
_DEFAULT_HL_PROTECTION = False
_DEFAULT_EV_COMP = 0.0
_DEFAULT_OFFSETS = (0, 1)


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        grey18, gamma, hl_protection, ev_comp, offsets = get_parameters({})

        self.assertEqual(grey18, _DEFAULT_GREY18)
        self.assertEqual(gamma, _DEFAULT_GAMMA)
        self.assertEqual(hl_protection, _DEFAULT_HL_PROTECTION)
        self.assertEqual(ev_comp, _DEFAULT_EV_COMP)
        self.assertEqual(offsets, _DEFAULT_OFFSETS)

    def test_get_parameters_grey18(self) -> None:
        grey18, _, _, _, _ = get_parameters({"grey18": [87, 87, 87]})
        self.assertEqual(grey18, [87, 87, 87])

    def test_get_parameters_gamma(self) -> None:
        _, gamma, _, _, _ = get_parameters({"gamma": 2.0})
        self.assertEqual(gamma, 2.0)

    def test_get_parameters_hl_protection(self) -> None:
        _, _, hl_protection, _, _ = get_parameters({"highlight_protection": True})
        self.assertEqual(hl_protection, True)

    def test_get_parameters_exposure_compensation(self) -> None:
        _, _, _, ev_comp, _ = get_parameters({"exposure_compensation": -1})
        self.assertEqual(ev_comp, -1)

    def test_get_parameters_matte_effect(self) -> None:
        _, _, _, _, offsets = get_parameters({"matte_effect": True})
        self.assertEqual(offsets, (16 / 255, 1.0))

    def test_marshal_curve(self) -> None:
        self.assertEqual(marshal_curve([]), {"Curve": "0;"})
        self.assertEqual(
            marshal_curve([Point(0, 0), Point(1, 1)]),
            {
                "Curve": "1;0.000000;0.000000;1.000000;1.000000;",
            },
        )
