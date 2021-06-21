from unittest import TestCase

from profile_generator.model import spline
from profile_generator.model.spline import Matrix

from .colorspace import (
    D50_XYZ,
    D65_TO_D50_ADAPTATION,
    D65_XYZ,
    PROPHOTO_REFS,
    PROPHOTO_TO_XYZ,
    SRGB_REFS,
    SRGB_TO_XYZ,
    XYZ_TO_PROPHOTO,
    XYZ_TO_SRGB,
    get_conversion_matrix,
    lab_to_lch,
    lab_to_xyz,
    lch_to_lab,
    normalize,
    srgb_to_prophoto,
    srgb_to_xyz,
    xyz_to_lab,
    xyz_to_srgb,
    xyz_to_xyy,
)


class ColorspaceTest(TestCase):
    def test_noramlize_rgb(self) -> None:
        self._assert_color_equal(normalize([0, 127, 255]), [0, 0.4980392, 1])

    def test_srgb_to_xyz(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], srgb_to_xyz([0.0, 0.0, 0.0]))
        self._assert_color_equal(D65_XYZ, srgb_to_xyz([1.0, 1.0, 1.0]))
        self._assert_color_equal(
            [0.1861276, 0.1969824, 0.5993615],
            srgb_to_xyz([0.02, 0.5, 0.8]),
        )

    def test_srgb_to_prophoto(self) -> None:
        self._assert_color_equal(
            [0.2485860, 0.2716272, 0.3247666], srgb_to_prophoto(normalize([87, 87, 87]))
        )

    def test_srgb_to_lab(self) -> None:
        srgb_to_lab = lambda color: xyz_to_lab(srgb_to_xyz(color))
        self._assert_color_equal([0.0, 0.0, 0.0], srgb_to_lab([0.0, 0.0, 0.0]))
        self._assert_color_equal([100.0, 0.0, 0.0], srgb_to_lab([1.0, 1.0, 1.0]))
        self._assert_color_equal(
            [52.2522841, 2.7790458, -46.2895491],
            srgb_to_lab([0.2, 0.5, 0.8]),
        )

    def test_lab_to_srgb(self) -> None:
        lab_to_srgb = lambda color: xyz_to_srgb(lab_to_xyz(color))
        self._assert_color_equal([0.0, 0.0, 0.0], lab_to_srgb([0.0, 0.0, 0.0]))
        self._assert_color_equal(
            [1.0, 0.5746288, 0.1939663], lab_to_srgb([100.0, 100.0, 100.0])
        )
        self._assert_color_equal(
            [0.5739409, 0.4558792, 0.0], lab_to_srgb([50.0, 0.0, 100.0])
        )
        self._assert_color_equal([1.0, 0.0, 0.4828316], lab_to_srgb([50.0, 100.0, 0.0]))

    def test_lab_to_lch(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], lab_to_lch([0.0, 0.0, 0.0]))
        self._assert_color_equal(
            [100.0, 141.4213562, 45.0], lab_to_lch([100.0, 100.0, 100.0])
        )
        self._assert_color_equal([50.0, 25.0, 90.0], lab_to_lch([50.0, 0.0, 25.0]))
        self._assert_color_equal([32.0, 25.0, 270.0], lab_to_lch([32.0, 0.0, -25.0]))
        self._assert_color_equal(
            [50.0, 22.3606798, 63.4349488], lab_to_lch([50.0, 10.0, 20.0])
        )
        self._assert_color_equal(
            [50.0, 22.3606798, 153.4349488], lab_to_lch([50.0, -20.0, 10.0])
        )
        self._assert_color_equal(
            [50.0, 20.6155281, 194.0362435], lab_to_lch([50.0, -20.0, -5.0])
        )

    def test_lch_to_lab(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], lch_to_lab([0.0, 0.0, 0.0]))
        self._assert_color_equal([100.0, 100.0, 0.0], lch_to_lab([100.0, 100.0, 360.0]))
        self._assert_color_equal(
            [50.0, 45.6772729, 20.3368322], lch_to_lab([50.0, 50.0, 24.0])
        )
        self._assert_color_equal([75.0, 0.0, -1], lch_to_lab([75.0, 1.0, 270.0]))

    def test_xyz_to_xyy(self) -> None:
        self._assert_color_equal([0.95047, 1.0, 0.0], xyz_to_xyy([0.0, 0.0, 0.0]))

    def test_chromatic_adaption(self) -> None:
        print(D65_TO_D50_ADAPTATION)
        self._assert_matrix_equal(
            [
                [1.047811272, 0.022886525, -0.050126939],
                [0.029542405, 0.990484461, -0.017049122],
                [-0.009234507, 0.015043570, 0.752131644],
            ],
            D65_TO_D50_ADAPTATION,
        )

    def test_get_conversion_matrix_srgb(self) -> None:
        matrix = get_conversion_matrix(SRGB_REFS, D65_XYZ)
        inverse = spline.inverse_matrix(list(matrix))

        self._assert_matrix_equal(SRGB_TO_XYZ, matrix)
        self._assert_matrix_equal(XYZ_TO_SRGB, inverse)

    def test_get_conversion_matrix_prophoto(self) -> None:
        matrix = get_conversion_matrix(PROPHOTO_REFS, D50_XYZ)
        inverse = spline.inverse_matrix(list(matrix))

        self._assert_matrix_equal(PROPHOTO_TO_XYZ, matrix)
        self._assert_matrix_equal(XYZ_TO_PROPHOTO, inverse)

    def _assert_color_equal(self, list1: list[float], list2: list[float]) -> None:
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b)

    def _assert_matrix_equal(self, matrix1: Matrix, matrix2: Matrix) -> None:
        for row1, row2 in zip(matrix1, matrix2):
            for a, b in zip(row1, row2):
                self.assertAlmostEqual(a, b, 9)
