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
                    "1;0.00000;0.50000;0.00000;0.19673;"
                    + "0.40000;0.60000;0.19673;0.00000;"
                    + "0.60000;0.60000;0.00000;0.19673;"
                    + "1.00000;0.50000;0.19673;0.00000;"
                ),
            },
            get_profile_args({"local": 20}),
        )
