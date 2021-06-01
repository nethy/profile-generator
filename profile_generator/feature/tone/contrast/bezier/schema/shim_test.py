import unittest
from unittest.mock import Mock

from . import shim
from .shim import Point, Strength

_DEFAULT_GREY = Point(92 / 255, 119 / 255)
_DEFAULT_WEIGHTS = (1, 1)


class ResolveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.calculate_mock = Mock(return_value=[Point(0, 0), Point(1, 1)])

    def test_get_arguments_default(self) -> None:
        self.assertTupleEqual(
            (_DEFAULT_GREY, Strength(0), _DEFAULT_WEIGHTS), shim.get_arguments({})
        )

    def test_get_arguments_middle_grey(self) -> None:
        self.assertTupleEqual(
            (Point(90 / 255, 128 / 255), Strength(), _DEFAULT_WEIGHTS),
            shim.get_arguments({"grey": {"x": 90, "y": 128}}),
        )

    def test_get_arguments_strength(self) -> None:
        self.assertTupleEqual(
            (_DEFAULT_GREY, Strength(0.1), _DEFAULT_WEIGHTS),
            shim.get_arguments({"strength": 10}),
        )

    def test_get_weights(self) -> None:
        self.assertTupleEqual(
            (_DEFAULT_GREY, Strength(), (3.14, 2.72)),
            shim.get_arguments({"weights": [3.14, 2.72]}),
        )

    def test_marshal_curve(self) -> None:
        self.assertEqual({"Curve": "0;"}, shim.marshal_curve([]))

        self.assertEqual(
            {"Curve": "4;0.000000;0.000000;1.000000;1.000000;"},
            shim.marshal_curve((Point(0, 0), Point(1, 1))),
        )
