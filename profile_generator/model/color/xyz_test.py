from profile_generator.model.color import illuminant
from profile_generator.model.color.profile import PROPHOTO, SRGB
from profile_generator.model.linalg_test import LinalgTestCase

from .xyz import chromatic_adaptation, from_rgb, to_rgb, to_xyy


class XyzTest(LinalgTestCase):
    def test_rgb_to_xyz(self) -> None:
        self.assert_vector_equal(from_rgb([0.0, 0.0, 0.0], SRGB), [0.0, 0.0, 0.0])
        self.assert_vector_equal(from_rgb([1.0, 1.0, 1.0], SRGB), illuminant.D50_XYZ, 5)
        self.assert_vector_equal(
            from_rgb([0.02, 0.5, 0.8], SRGB),
            [0.1694955, 0.1903918, 0.4520303],
        )
        self.assert_vector_equal(
            from_rgb([1.0, 1.0, 1.0], PROPHOTO), illuminant.D50_XYZ
        )

    def test_xyz_to_rgb(self) -> None:
        self.assert_vector_equal(
            [0.02, 0.6, 1], to_rgb(from_rgb([0.02, 0.6, 1], SRGB), SRGB), 5
        )
        self.assert_vector_equal(
            [0.02, 0.6, 1], to_rgb(from_rgb([0.02, 0.6, 1], PROPHOTO), PROPHOTO)
        )

    def test_xyz_to_xyy(self) -> None:
        self.assert_vector_equal(to_xyy([0.0, 0.0, 0.0]), [0.9504301, 1.0, 0.0])

    def test_chromatic_adaption(self) -> None:
        self.assert_matrix_equal(
            chromatic_adaptation(illuminant.D65_XYZ, illuminant.D50_XYZ),
            [
                [1.0478371, 0.0229006, -0.0501324],
                [0.0295635, 0.9904682, -0.0170519],
                [-0.0092342, 0.0150422, 0.7521286],
            ],
        )
