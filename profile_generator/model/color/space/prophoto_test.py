from profile_generator.model import linalg
from profile_generator.model.color import xyz
from profile_generator.model.linalg_test import LinalgTestCase

from . import prophoto


class ProphotoTest(LinalgTestCase):
    def test_matrixes(self) -> None:
        matrix = xyz.conversion_matrix_of(
            prophoto.PROPHOTO_XY, prophoto.PROPHOTO.white_point
        )
        inverse = linalg.inverse(matrix)

        self.assert_matrix_equal(prophoto.PROPHOTO.xyz_matrix, matrix)
        self.assert_matrix_equal(prophoto.PROPHOTO.xyz_inverse_matrix, inverse)
