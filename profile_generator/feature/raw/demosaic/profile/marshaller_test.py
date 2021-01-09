import unittest

from .marshaller import get_profile_args


class MarshallerTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual({"BAYER_METHOD": "rcdvng4"}, get_profile_args({}))

    def test_demosaic(self) -> None:
        self.assertEqual(
            {"BAYER_METHOD": "rcdvng4"}, get_profile_args({"demosaic": "RCD+VNG4"})
        )

        self.assertEqual(
            {"BAYER_METHOD": "rcdvng4"}, get_profile_args({"demosaic": "rcd+vng4"})
        )

        self.assertEqual(
            {"BAYER_METHOD": "lmmse"}, get_profile_args({"demosaic": "LMMSE"})
        )
