import unittest

from .marshaller import get_profile_args

_DEFAULT = {
    "DenoiseEnabled": "false",
    "DenoiseSMethod": "shal",
    "DenoiseLCurve": "0;",
    "DenoiseCCCurve": "0;",
    "ImpulseDenoiseEnabled": "false",
}


class NoiseMarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            _DEFAULT,
            get_profile_args({}),
        )

    def test_luminance(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "DenoiseEnabled": "true",
                "DenoiseLCurve": (
                    "1;0.000000;0.400000;0.000000;0.000000;"
                    + "0.750000;0.100000;0.425651;0.000000;"
                ),
            },
            get_profile_args({"luminance": 40}),
        )

    def test_chrominance(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "DenoiseEnabled": "true",
                "DenoiseCCCurve": (
                    "1;0.000000;0.400000;0.000000;0.468750;"
                    + "0.200000;0.000000;0.468750;0.000000;"
                ),
            },
            get_profile_args({"chrominance": 40}),
        )

    def test_mode(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "DenoiseSMethod": "shal"},
            get_profile_args({"mode": "Conservative"}),
        )

        self.assertEqual(
            {**_DEFAULT, "DenoiseSMethod": "shalbi", "ImpulseDenoiseEnabled": "true"},
            get_profile_args({"mode": "Aggressive"}),
        )
