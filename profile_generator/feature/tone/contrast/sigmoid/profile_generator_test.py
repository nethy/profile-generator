from unittest import TestCase
from unittest.mock import Mock, patch

from profile_generator.feature.tone.contrast.sigmoid.profile_generator import generate
from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.color import constants
from profile_generator.unit.point import Point

_CONTRAST_SIGMOID = (
    "profile_generator.feature.tone.contrast.sigmoid.profile_generator.contrast_sigmoid"
)
_CONTRAST_SIGMOID_GET_TONE_CURVE = f"{_CONTRAST_SIGMOID}.get_tone_curve"


class ProfileGeneratorTest(TestCase):
    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    def test_default(self, get_tone_curve: Mock) -> None:
        get_tone_curve.return_value = [Point(1, 1)]

        self.assertEqual(
            generate(ProfileParams(), False),
            {
                "Curve": "0;",
            },
        )
        get_tone_curve.assert_called_once_with(constants.GREY18_LINEAR, 1.0)

    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    def test(self, get_tone_curve: Mock) -> None:
        get_tone_curve.return_value = [Point(1, 1)]

        profile_params = ProfileParams()
        profile_params.tone.curve.sigmoid.parse({"linear_grey18": 0.1, "slope": 1.6})

        self.assertEqual(
            generate(profile_params, False),
            {
                "Curve": "4;1.0000000;1.0000000;",
            },
        )
        get_tone_curve.assert_called_once_with(0.1, 1.6)
