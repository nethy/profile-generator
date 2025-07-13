from profile_generator.model.color import xyz
from profile_generator.model.linalg_test import LinalgTestCase

from .illuminant import D50_XYZ, D65_XYZ


class IlluminantTest(LinalgTestCase):
    def test_d65(self) -> None:
        self.assert_vector_equal(xyz.from_xyy([0.31272, 0.32903, 1.0]), D65_XYZ, 28)

    def test_d50(self) -> None:
        self.assert_vector_equal(xyz.from_xyy([0.34567, 0.35850, 1.0]), D50_XYZ, 28)
