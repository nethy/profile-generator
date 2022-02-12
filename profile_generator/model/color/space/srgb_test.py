from profile_generator.model import linalg
from profile_generator.model.color import xyz
from profile_generator.model.linalg_test import LinalgTestCase

from . import srgb


class SrgbTest(LinalgTestCase):
    def test_matrixes(self) -> None:
        matrix = xyz.conversion_matrix_of(srgb.SRGB_XY, srgb.SRGB.white_point)
        inverse = linalg.inverse(matrix)

        self.assert_matrix_equal(srgb.SRGB.xyz_matrix, matrix)
        self.assert_matrix_equal(srgb.SRGB.xyz_inverse_matrix, inverse)

    def test_gamma(self) -> None:
        for luminance in (i / 100 for i in range(101)):
            self.assertAlmostEqual(srgb.inverse_gamma(srgb.gamma(luminance)), luminance)

    def test_gamma_middle_grey(self) -> None:
        self.assertAlmostEqual(srgb.gamma(0.18), 0.4613561)
