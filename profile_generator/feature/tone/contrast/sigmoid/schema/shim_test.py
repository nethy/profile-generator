from unittest import TestCase

from .shim import Point, get_parameters, marshal_curves

_DEFAULT_GAMMA = 1.0
_DEFAULT_NEUTRAL5 = [90.0, 90.0, 90.0]
_DEFAULT_EV_COMP = 0.0


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        netrual5, gamma, ev_comp, offsets = get_parameters({})

        self.assertEqual(netrual5, _DEFAULT_NEUTRAL5)
        self.assertEqual(gamma, _DEFAULT_GAMMA)
        self.assertEqual(ev_comp, _DEFAULT_EV_COMP)
        self.assertEqual(offsets, (0, 1))

    def test_get_parameters_neutral5(self) -> None:
        neutral5, _, _, _ = get_parameters({"neutral5": [87, 87, 87]})
        self.assertEqual(neutral5, [87, 87, 87])

    def test_get_parameters_gamma(self) -> None:
        _, gamma, _, _ = get_parameters({"gamma": 2.0})
        self.assertEqual(gamma, 2.0)

    def test_get_parameters_exposure_compensation(self) -> None:
        _, _, ev_comp, _ = get_parameters({"exposure_compensation": -1})
        self.assertEqual(ev_comp, -1)

    def test_get_parameters_matte_effect(self) -> None:
        _, _, _, offsets = get_parameters({"matte_effect": True})
        self.assertEqual(offsets, (16 / 255, 1.0))

    def test_marshal_curves(self) -> None:
        self.assertEqual(marshal_curves([], []), {"Curve": "0;", "Curve2": "0;"})
        self.assertEqual(
            marshal_curves([Point(0, 0), Point(1, 1)], [Point(0, 0), Point(1, 1)]),
            {
                "Curve": "3;0.000000;0.000000;1.000000;1.000000;",
                "Curve2": "1;0.000000;0.000000;1.000000;1.000000;",
            },
        )
