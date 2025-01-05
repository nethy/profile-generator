from unittest import TestCase

from profile_generator.main.profile_params import ProfileParams

from .demosaic import profile_generator_test as demosaic_test
from .profile_generator import generate

DEFAULT = {
    "BayerPreBlackRed": "0",
    "BayerPreBlackGreen": "0",
    "BayerPreBlackBlue": "0",
    **demosaic_test.DEFAULT,
}


class ProfileGeneratorTest(TestCase):
    def test_generate_defaults(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.parse({})
        self.assertEqual(generate(profile_params), DEFAULT)

    def test_generate_black_points(self) -> None:
        profile_params = ProfileParams()
        profile_params.raw.parse({"black_points": [-1, 1, 2]})
        self.assertEqual(
            generate(profile_params),
            {
                **DEFAULT,
                "BayerPreBlackRed": "-1",
                "BayerPreBlackGreen": "1",
                "BayerPreBlackBlue": "2",
            },
        )
