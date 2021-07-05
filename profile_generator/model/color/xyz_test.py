from profile_generator.model.color import white_point
from profile_generator.model.color.space import PROPHOTO, SRGB
from profile_generator.model.linalg_test import LinalgTestCase

from .xyz import D65_TO_D50_ADAPTATION, from_rgb, to_rgb, to_xyy


class XyzTest(LinalgTestCase):
    def test_rgb_to_xyz(self) -> None:
        self.assert_vector_equal(from_rgb([0.0, 0.0, 0.0], SRGB), [0.0, 0.0, 0.0])
        self.assert_vector_equal(from_rgb([1.0, 1.0, 1.0], SRGB), white_point.D65_XYZ)
        self.assert_vector_equal(
            from_rgb([0.02, 0.5, 0.8], SRGB),
            [0.1861276, 0.1969824, 0.5993615],
        )
        self.assert_vector_equal(
            from_rgb([1.0, 1.0, 1.0], PROPHOTO), white_point.D50_XYZ
        )

    def test_xyz_to_rgb(self) -> None:
        self.assert_vector_equal(
            [0.02, 0.6, 1], to_rgb(from_rgb([0.02, 0.6, 1], SRGB), SRGB)
        )
        self.assert_vector_equal(
            [0.02, 0.6, 1], to_rgb(from_rgb([0.02, 0.6, 1], PROPHOTO), PROPHOTO)
        )

    def test_xyz_to_xyy(self) -> None:
        self.assert_vector_equal(to_xyy([0.0, 0.0, 0.0]), [0.95047, 1.0, 0.0])

    def test_chromatic_adaption(self) -> None:
        self.assert_matrix_equal(
            [
                [1.047811272, 0.022886525, -0.050126939],
                [0.029542405, 0.990484461, -0.017049122],
                [-0.009234507, 0.015043570, 0.752131644],
            ],
            D65_TO_D50_ADAPTATION,
        )
