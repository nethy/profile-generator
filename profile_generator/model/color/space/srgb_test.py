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
