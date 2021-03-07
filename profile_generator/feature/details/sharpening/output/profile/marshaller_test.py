import unittest
from typing import Any, Dict

from .marshaller import get_profile_args

_DEFAULT = {
    "SharpeningEnabled": "false",
    "SharpeningContrast": "20",
    "DeconvRadius": "0.75",
    "DeconvAmount": "100",
    "DeconvIterations": "30",
}


class MarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            _DEFAULT,
            get_profile_args({}),
        )

    def test_enabled(self) -> None:
        self._assert_profile_args({"enabled": True}, SharpeningEnabled="true")
        self._assert_profile_args({"enabled": False}, SharpeningEnabled="false")

    def test_threshold(self) -> None:
        self._assert_profile_args({"threshold": 0}, SharpeningContrast="0")
        self._assert_profile_args({"threshold": 200}, SharpeningContrast="200")

    def test_radius(self) -> None:
        self._assert_profile_args({"radius": 0.4}, DeconvRadius="0.40")
        self._assert_profile_args({"radius": 2.5}, DeconvRadius="2.50")

    def test_amount(self) -> None:
        self._assert_profile_args({"amount": 0}, DeconvAmount="0")
        self._assert_profile_args({"amount": 100}, DeconvAmount="100")

    def test_iterations(self) -> None:
        self._assert_profile_args({"iterations": 5}, DeconvIterations="5")
        self._assert_profile_args({"iterations": 100}, DeconvIterations="100")

    def _assert_profile_args(
        self, config: Dict[str, Any], **expect_output: str
    ) -> None:
        self.assertEqual({**_DEFAULT, **expect_output}, get_profile_args(config))
