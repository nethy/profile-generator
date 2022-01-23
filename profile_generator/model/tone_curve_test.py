from unittest import TestCase

from profile_generator.model.color import constants

from .tone_curve import filmic

_GREY_18 = 87 / 255


class TestToneCurve(TestCase):
    def test_filmic(self) -> None:
        _curve = filmic(_GREY_18, 2)

        self.assertAlmostEqual(_curve(0), 0)
        self.assertAlmostEqual(_curve(0.2), 0.1540329)
        self.assertAlmostEqual(_curve(_GREY_18), constants.LUMINANCE_50_SRGB)
        self.assertAlmostEqual(_curve(0.8), 0.9549321)
        self.assertAlmostEqual(_curve(1), 1)
