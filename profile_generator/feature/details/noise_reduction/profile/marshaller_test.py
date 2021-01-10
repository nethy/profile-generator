import unittest

from .marshaller import get_profile_args

_DEFAULT = {
    "DenoisingEnabled": "false",
    "DenoisingLCurve": "1;0.2;0.10;0;0;1;0;0;0;",
    "Median": "false",
}


class MarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            _DEFAULT,
            get_profile_args({}),
        )

    def test_enabled(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "DenoisingEnabled": "true"},
            get_profile_args({"enabled": True}),
        )

    def test_strength(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "DenoisingLCurve": "1;0.2;0.33;0;0;1;0;0;0;"},
            get_profile_args({"strength": 33}),
        )

    def test_median(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "Median": "true"},
            get_profile_args({"median": True}),
        )
