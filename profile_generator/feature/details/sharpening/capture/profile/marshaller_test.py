import unittest

from .marshaller import get_profile_args


class MarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual({"CaptureSharpeningEnabled": "false"}, get_profile_args({}))

    def test_enabled(self) -> None:
        self.assertEqual(
            {"CaptureSharpeningEnabled": "true"}, get_profile_args({"enabled": True})
        )
        self.assertEqual(
            {"CaptureSharpeningEnabled": "false"}, get_profile_args({"enabled": False})
        )
