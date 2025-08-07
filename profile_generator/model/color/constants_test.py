from profile_generator.model.linalg_test import LinalgTestCase

from .constants import GREY18_LINEAR, GREY18_SRGB


class ConstantsTestCase(LinalgTestCase):
    def test_grey18_lienar(self) -> None:
        self.assertAlmostEqual(GREY18_LINEAR, 0.1841865)

    def test_grey18_rgb(self) -> None:
        self.assertAlmostEqual(GREY18_SRGB, 0.4663266)
