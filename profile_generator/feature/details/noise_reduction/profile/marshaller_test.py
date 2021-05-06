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
                    "1;0.00000;0.40000;0.00000;0.00000;"
                    + "0.75000;0.10000;0.42565;0.00000;"
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
                    "1;0.00000;0.40000;0.00000;0.46875;"
                    + "0.20000;0.00000;0.46875;0.00000;"
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
