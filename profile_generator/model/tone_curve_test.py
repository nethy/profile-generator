from unittest import TestCase

from profile_generator.model.color import constants
from profile_generator.model.color.space import SRGB

from .tone_curve import get_rgb_contrast, get_rgb_flat

_GREY_18 = 0.1


class TestToneCurve(TestCase):
    def test_srgb_flat(self) -> None:
        curve = get_rgb_flat(_GREY_18)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(1), 1)
        self.assertAlmostEqual(curve(SRGB.gamma(_GREY_18)), constants.GREY18_RGB)
        self.assertAlmostEqual(curve(0.2), 0.2861168)
        self.assertAlmostEqual(curve(0.8), 0.8596069)

    def test_srgb_contrast(self) -> None:
        curve = get_rgb_contrast(2)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(1), 1)
        self.assertAlmostEqual(curve(constants.GREY18_RGB), constants.GREY18_RGB)
        self.assertAlmostEqual(curve(0.2), 0.0444980)
        self.assertAlmostEqual(curve(0.8), 0.9159756)
