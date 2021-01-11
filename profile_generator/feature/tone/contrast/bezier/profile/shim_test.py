import unittest
from unittest.mock import Mock

from . import shim
from .shim import Point, Strength

_DEFAULT_GREY = Point(92 / 255, 119 / 255)


class ResolveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.calculate_mock = Mock(return_value=[Point(0, 0), Point(1, 1)])

    def test_get_arguments_default(self) -> None:
        self.assertTupleEqual((_DEFAULT_GREY, Strength(0)), shim.get_arguments({}))

    def test_get_arguments_middle_grey(self) -> None:
        self.assertTupleEqual(
            (Point(90 / 255, 128 / 255), Strength()),
            shim.get_arguments({"middle_grey": [90, 128]}),
        )

    def test_get_arguments_strength(self) -> None:
        self.assertTupleEqual(
            (_DEFAULT_GREY, Strength(0.1)), shim.get_arguments({"strength": 10})
        )

    def test_marshal_points(self) -> None:
        self.assertEqual({"Curve": "0;"}, shim.marshal_curve([]))

        self.assertEqual(
            {"Curve": "1;0.00000;0.00000;1.00000;1.00000;"},
            shim.marshal_curve((Point(0, 0), Point(1, 1))),
        )
