from unittest import TestCase

from .marshaller import get_profile_args

_CURVE_TEMPLATE = "1;0;0.5;0;0.25;0.4;{value};0.25;0;0.6;{value};0;0.25;1;0.5;0.25;0;"


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
                "OpacityCurveWL": _CURVE_TEMPLATE.format(value="0.60000"),
            },
            get_profile_args({"local": 20}),
        )
