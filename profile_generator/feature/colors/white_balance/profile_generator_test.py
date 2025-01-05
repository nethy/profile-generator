from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {
    "WBSetting": "Camera",
    "WBTemperature": "6504",
    "WBGreen": "1",
}


class ProfileGeneratorTest(TestCase):
    def test_process_wb_temperature(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.white_balance.parse({"temperature": 5500})
        self.assertEqual(
            generate(profile_params),
            {**DEFAULT, "WBSetting": "Custom", "WBTemperature": "5500"},
        )

    def test_process_wb_tint(self) -> None:
        profile_params = ProfileParams()
        profile_params.colors.white_balance.parse({"tint": 0.880})
        self.assertEqual(
            generate(profile_params),
            {**DEFAULT, "WBSetting": "Custom", "WBGreen": "0.88"},
        )
