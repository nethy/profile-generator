from unittest import TestCase

from .shim import Point, get_parameters, marshal_curve

_DEFAULT_GAMMA = 1.0
_DEFAULT_HLP = 1.0
_DEFAULT_GREY_X = 90 / 255
_DEFAULT_GREY_Y = 365 / 3 / 255


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        grey, gamma, hlp, offsets = get_parameters({})

        self.assertEqual(grey, Point(_DEFAULT_GREY_X, _DEFAULT_GREY_Y))
        self.assertEqual(gamma, _DEFAULT_GAMMA)
        self.assertEqual(hlp, _DEFAULT_HLP)
        self.assertEqual(offsets, (0, 1))

    def test_get_parameters_neutral5(self) -> None:
        grey, _, _, _ = get_parameters({"neutral5": [87, 87, 87]})
        self.assertEqual(grey, Point(87 / 255, _DEFAULT_GREY_Y))

    def test_get_parameters_exposure_compensation(self) -> None:
        grey, _, _, _ = get_parameters({"exposure_compensation": -1})
        self.assertEqual(grey, Point(_DEFAULT_GREY_X, 0.343643))

        grey, _, _, _ = get_parameters({"exposure_compensation": 1})
        self.assertEqual(grey, Point(_DEFAULT_GREY_X, 0.655301))

    def test_get_parameters_gamma(self) -> None:
        _, gamma, _, _ = get_parameters({"gamma": 2.0})
        self.assertEqual(2.0, gamma)

    def test_get_parameters_highlight_protection(self) -> None:
        _, _, hlp, _ = get_parameters({"highlight_protection": 2.0})
        self.assertEqual(2.0, hlp)

    def test_get_parameters_matte_effect(self) -> None:
        _, _, _, offsets = get_parameters({"matte_effect": True})
        self.assertEqual((16 / 255, 235 / 255), offsets)

    def test_marshal_curve(self) -> None:
        self.assertEqual({"Curve": "0;"}, marshal_curve([]))
        self.assertEqual(
            {"Curve": "1;0.000000;0.000000;1.000000;1.000000;"},
            marshal_curve([Point(0, 0), Point(1, 1)]),
        )
