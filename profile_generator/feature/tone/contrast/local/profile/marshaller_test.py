from unittest import TestCase

from .marshaller import get_profile_args


class MarshallerTest(TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            {"WaveletEnabled": "false", "OpacityCurveWL": "0;"}, get_profile_args({})
        )

    def test_local(self) -> None:
        self.assertEqual(
            {"WaveletEnabled": "false", "OpacityCurveWL": "0;"},
            get_profile_args({"local": 0}),
        )
        self.assertEqual(
            {
                "WaveletEnabled": "true",
                "OpacityCurveWL": (
                    "1;0.000000;0.500000;0.000000;0.146447;"
                    + "0.400000;0.600000;0.146447;0.000000;"
                    + "0.600000;0.600000;0.000000;0.146447;"
                    + "1.000000;0.500000;0.146447;0.000000;"
                ),
            },
            get_profile_args({"local": 20}),
        )
