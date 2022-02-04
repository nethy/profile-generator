from unittest import TestCase

from .shim import Point, get_parameters, marshal

_DEFAULT_GREY18 = 90.0
_DEFAULT_SLOPE = 1.0


class ShimTest(TestCase):
    def test_get_parameters_defaults(self) -> None:
        grey18, slope = get_parameters({})

        self.assertEqual(grey18, _DEFAULT_GREY18)
        self.assertEqual(slope, _DEFAULT_SLOPE)

    def test_get_parameters_grey18(self) -> None:
        grey18, _ = get_parameters({"grey18": [87, 87, 87]})
        self.assertEqual(grey18, [87, 87, 87])

    def test_get_parameters_slope(self) -> None:
        _, slope = get_parameters({"slope": 2.0})
        self.assertEqual(slope, 2.0)

    def test_marshal(self) -> None:
        self.assertEqual(marshal([]), {"Curve": "0;"})
        self.assertEqual(
            marshal([Point(0, 0), Point(1, 1)]),
            {"Curve": "1;0.000000;0.000000;1.000000;1.000000;"},
        )
