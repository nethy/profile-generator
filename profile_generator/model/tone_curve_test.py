from unittest import TestCase

from profile_generator.model.color import constants

from .tone_curve import filmic

_GREY_18 = 87 / 255


class TestToneCurve(TestCase):
    def test_filmic_flat(self) -> None:
        flat, _ = filmic(_GREY_18, 2)

        self.assertAlmostEqual(flat(0), 0)
        self.assertAlmostEqual(flat(0.2), 0.2998106)
        self.assertAlmostEqual(flat(_GREY_18), constants.LUMINANCE_50_SRGB)
        self.assertAlmostEqual(flat(0.8), 0.8668710)
        self.assertAlmostEqual(flat(1), 1)

    def test_filmic_contrast(self) -> None:
        _, contrast = filmic(_GREY_18, 2)

        self.assertAlmostEqual(contrast(0), 0)
        self.assertAlmostEqual(contrast(0.2), 0.0745394)
        self.assertAlmostEqual(
            contrast(constants.LUMINANCE_50_SRGB), constants.LUMINANCE_50_SRGB
        )
        self.assertAlmostEqual(contrast(0.8), 0.8994821)
        self.assertAlmostEqual(contrast(1), 1)
