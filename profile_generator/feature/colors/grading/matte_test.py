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
