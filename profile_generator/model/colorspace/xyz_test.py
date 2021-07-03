from profile_generator.model import linalg
from profile_generator.model.linalg import Matrix

from . import rgb
from .colorspacetest import ColorspaceTest
from .xyz import (
    D50_XYZ,
    D65_TO_D50_ADAPTATION,
    D65_XYZ,
    PROPHOTO_TO_XYZ,
    PROPHOTO_XY,
    SRGB_TO_XYZ,
    SRGB_XY,
    XYZ_TO_PROPHOTO,
    XYZ_TO_SRGB,
    get_conversion_matrix,
    srgb_to_prophoto,
    srgb_to_xyz,
    xyz_to_xyy,
)


class XyzTest(ColorspaceTest):
    def test_srgb_to_xyz(self) -> None:
        self.assert_color_equal(srgb_to_xyz([0.0, 0.0, 0.0]), [0.0, 0.0, 0.0])
        self.assert_color_equal(srgb_to_xyz([1.0, 1.0, 1.0]), D65_XYZ)
        self.assert_color_equal(
            srgb_to_xyz([0.02, 0.5, 0.8]),
            [0.1861276, 0.1969824, 0.5993615],
        )

    def test_srgb_to_prophoto(self) -> None:
        self.assert_color_equal(
            srgb_to_prophoto(rgb.normalize([87, 87, 87])),
            [0.2485860, 0.2716272, 0.3247666],
        )

    def test_xyz_to_xyy(self) -> None:
        self.assert_color_equal(xyz_to_xyy([0.0, 0.0, 0.0]), [0.95047, 1.0, 0.0])

    def test_chromatic_adaption(self) -> None:
        self._assert_matrix_equal(
            [
                [1.047811272, 0.022886525, -0.050126939],
                [0.029542405, 0.990484461, -0.017049122],
                [-0.009234507, 0.015043570, 0.752131644],
            ],
            D65_TO_D50_ADAPTATION,
        )

    def test_get_conversion_matrix_srgb(self) -> None:
        matrix = get_conversion_matrix(SRGB_XY, D65_XYZ)
        inverse = linalg.inverse(list(matrix))

        self._assert_matrix_equal(SRGB_TO_XYZ, matrix)
        self._assert_matrix_equal(XYZ_TO_SRGB, inverse)

    def test_get_conversion_matrix_prophoto(self) -> None:
        matrix = get_conversion_matrix(PROPHOTO_XY, D50_XYZ)
        inverse = linalg.inverse(list(matrix))

        self._assert_matrix_equal(PROPHOTO_TO_XYZ, matrix)
        self._assert_matrix_equal(XYZ_TO_PROPHOTO, inverse)

    def _assert_matrix_equal(self, matrix1: Matrix, matrix2: Matrix) -> None:
        for row1, row2 in zip(matrix1, matrix2):
            for a, b in zip(row1, row2):
                self.assertAlmostEqual(a, b, 9)
