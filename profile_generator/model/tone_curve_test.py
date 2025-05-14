from unittest import TestCase

from profile_generator.model.color import constants
from profile_generator.model.color.space import srgb

from .tone_curve import get_srgb_contrast, get_srgb_flat

_GREY_18 = 87 / 255


class TestToneCurve(TestCase):
    def test_srgb_flat(self) -> None:
        curve = get_srgb_flat(_GREY_18)
        print(srgb.inverse_gamma(_GREY_18))

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(1), 1)
        self.assertAlmostEqual(curve(_GREY_18), constants.GREY18_SRGB)
        self.assertAlmostEqual(curve(0.2), 0.2845130)
        self.assertAlmostEqual(curve(0.8), 0.8634577)

    def test_srgb_contrast(self) -> None:
        curve = get_srgb_contrast(2)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(1), 1)
        self.assertAlmostEqual(curve(constants.GREY18_SRGB), constants.GREY18_SRGB)
        self.assertAlmostEqual(curve(0.2), 0.0564814)
        self.assertAlmostEqual(curve(0.8), 0.8982875)
