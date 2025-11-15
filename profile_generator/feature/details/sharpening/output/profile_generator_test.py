from typing import Any
from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

_DEFAULT = {
    "SharpeningEnabled": "false",
    "SharpeningContrast": "20",
    "DeconvRadius": "0.75",
    "DeconvAmount": "0",
    "DeconvDamping": "5",
    "DeconvIterations": "10",
}


class ProfileGeneratorTest(TestCase):
    def test_default(self) -> None:
        params = ProfileParams()
        params.parse({})

        self.assertEqual(generate(params, False), _DEFAULT)

    def test_process_threshold(self) -> None:
        self._assert_process({"threshold": 0}, SharpeningContrast="0")
        self._assert_process({"threshold": 200}, SharpeningContrast="200")

    def test_process_radius(self) -> None:
        self._assert_process({"radius": 0.4}, DeconvRadius="0.40")
        self._assert_process({"radius": 2.5}, DeconvRadius="2.50")

    def test_process_amount(self) -> None:
        self._assert_process({"amount": 0}, DeconvAmount="0")
        self._assert_process(
            {"amount": 100}, SharpeningEnabled="true", DeconvAmount="100"
        )

    def test_process_damping(self) -> None:
        self._assert_process({"damping": 0}, DeconvDamping="0")
        self._assert_process({"damping": 100}, DeconvDamping="100")

    def test_process_iterations(self) -> None:
        self._assert_process({"iterations": 5}, DeconvIterations="5")
        self._assert_process({"iterations": 100}, DeconvIterations="100")

    def _assert_process(self, data: Any, **expected_output: str) -> None:
        params = ProfileParams()
        params.details.sharpening.output.parse(data)

        self.assertEqual(generate(params, False), _DEFAULT | expected_output)
