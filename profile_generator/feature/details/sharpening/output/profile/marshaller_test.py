import unittest

from .marshaller import get_profile_args

_DEFAULT = {
    "SharpeningEnabled": "false",
    "SharpeningContrast": "20",
    "DeconvRadius": "0.75",
}


class MarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(
            _DEFAULT,
            get_profile_args({}),
        )

    def test_enabled(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "SharpeningEnabled": "true",
            },
            get_profile_args({"enabled": True}),
        )

        self.assertEqual(
            {
                **_DEFAULT,
                "SharpeningEnabled": "false",
            },
            get_profile_args({"enabled": False}),
        )

    def test_threshold(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "SharpeningContrast": "0",
            },
            get_profile_args({"threshold": 0}),
        )

        self.assertEqual(
            {
                **_DEFAULT,
                "SharpeningContrast": "200",
            },
            get_profile_args({"threshold": 200}),
        )
