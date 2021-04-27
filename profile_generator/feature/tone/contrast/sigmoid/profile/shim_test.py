from unittest import TestCase

from .shim import Point, Strength, get_parameters, marshal_curve

_DEFAULT_STRENGTH = Strength(0)
_DEFAULT_GREY_X = 92 / 255
_DEFAULT_GREY_Y = 119 / 255


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        grey, strength = get_parameters({})

        self.assertEqual(Point(_DEFAULT_GREY_X, _DEFAULT_GREY_Y), grey)
        self.assertEqual(_DEFAULT_STRENGTH, strength)

    def test_get_parameters_grey(self) -> None:
        grey, _ = get_parameters({"grey": {"x": 75}})
        self.assertEqual(Point(75 / 255, _DEFAULT_GREY_Y), grey)

        grey, _ = get_parameters({"grey": {"y": 75}})
        self.assertEqual(Point(_DEFAULT_GREY_X, 75 / 255), grey)

        grey, _ = get_parameters({"grey": {"x": 75, "y": 87}})
        self.assertEqual(Point(75 / 255, 87 / 255), grey)

    def test_get_parameters_strength(self) -> None:
        _, strength = get_parameters({"strength": 49})
        self.assertEqual(Strength(0.49), strength)

    def test_marshal_curve(self) -> None:
        self.assertEqual({"Curve": "0;"}, marshal_curve([]))
        self.assertEqual(
            {"Curve": "1;0.00000;0.00000;1.00000;1.00000;"},
            marshal_curve([Point(0, 0), Point(1, 1)]),
        )
