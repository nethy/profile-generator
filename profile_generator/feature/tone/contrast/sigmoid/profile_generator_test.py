from unittest import TestCase
from unittest.mock import Mock, patch

from profile_generator.feature.tone.contrast.sigmoid.profile_generator import generate
from profile_generator.main.profile_params import ProfileParams
from profile_generator.unit.point import Point

_CONTRAST_SIGMOID = (
    "profile_generator.feature.tone.contrast.sigmoid.profile_generator.contrast_sigmoid"
)
_CONTRAST_SIGMOID_GET_TONE_CURVE = f"{_CONTRAST_SIGMOID}.get_tone_curve"


class ProfileGeneratorTest(TestCase):
    @patch(_CONTRAST_SIGMOID_GET_TONE_CURVE)
    def test(self, get_tone_curve: Mock) -> None:
        get_tone_curve.return_value = [Point(1, 1)]

        self.assertEqual(
            generate(ProfileParams()),
            {
                "Curve": "4;1.0000000;1.0000000;",
            },
        )
        get_tone_curve.assert_called_once_with(0.1, 1.6)
