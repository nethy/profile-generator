import unittest

from .marshaller import get_profile_args

_DEFAULT = {
    "DenoiseEnabled": "false",
    "DenoiseLCurve": (
        "1;0.20000;0.10000;0.31606;0.11060;1.00000;0.00000;0.11060;0.31606;"
    ),
    "DenoiseCCCurve": (
        "1;0.00000;0.50000;0.36820;0.49084;0.25000;0.00000;0.49084;0.36820;"
    ),
    "Median": "false",
}


class NoiseMarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            _DEFAULT,
            get_profile_args({}),
        )

    def test_enabled(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "DenoiseEnabled": "true"},
            get_profile_args({"enabled": True}),
        )

    def test_strength(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "DenoiseLCurve": (
                    "1;0.20000;0.33000;0.48156;0.28088;1.00000;0.00000;0.28088;0.48156;"
                ),
            },
            get_profile_args({"strength": 33}),
        )

    def test_median(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "Median": "true"},
            get_profile_args({"median": True}),
        )
