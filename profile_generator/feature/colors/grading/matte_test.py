from unittest import TestCase

from profile_generator.main.profile_params import Matte

from .matte import get_matte_curve


class MatteTest(TestCase):
    def test_matte_default(self) -> None:
        params = Matte()
        params.parse({})

        curve = get_matte_curve(params)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.25), 0.25)
        self.assertAlmostEqual(curve(0.5), 0.5)
        self.assertAlmostEqual(curve(0.75), 0.75)
        self.assertAlmostEqual(curve(1), 1)

    def test_matte(self) -> None:
        params = Matte()
        params.parse({"black": 10, "white": 90})

        curve = get_matte_curve(params)

        self.assertAlmostEqual(curve(0), 0.1)
        self.assertAlmostEqual(curve(0.1), 0.1159231)
        self.assertAlmostEqual(curve(0.5), 0.5)
        self.assertAlmostEqual(curve(0.9), 0.8840769)
        self.assertAlmostEqual(curve(1), 0.9)
