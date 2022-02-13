from unittest import TestCase

from profile_generator.model.color import constants

from .tone_curve import contrast, flat

_GREY_18 = 87 / 255


class TestToneCurve(TestCase):
    def test_flat(self) -> None:
        curve = flat(_GREY_18)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.2), 0.2884879)
        self.assertAlmostEqual(curve(_GREY_18), constants.GREY18_SRGB)
        self.assertAlmostEqual(curve(0.8), 0.8778418)
        self.assertAlmostEqual(curve(1), 1)

    def test_contrast(self) -> None:
        curve = contrast(_GREY_18, 2)

        self.assertAlmostEqual(curve(0), 0)
        self.assertAlmostEqual(curve(0.2), 0.0830341)
        self.assertAlmostEqual(curve(constants.GREY18_SRGB), constants.GREY18_SRGB)
        self.assertAlmostEqual(curve(0.8), 0.9107727)
        self.assertAlmostEqual(curve(1), 1)
