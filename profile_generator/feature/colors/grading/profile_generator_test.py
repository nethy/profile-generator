from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .profile_generator import generate

DEFAULT = {
    "RGBCurvesEnabled": "false",
    "RGBCurvesRCurve": "0;",
    "RGBCurvesGCurve": "0;",
    "RGBCurvesBCurve": "0;",
}


class ProfileGeneratorTest(TestCase):
    def test_generate_default(self) -> None:
        params = ProfileParams()
        params.parse({})

        self.assertDictEqual(generate(params), DEFAULT)
