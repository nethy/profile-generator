from profile_generator.model.linalg_test import LinalgTestCase
from profile_generator.unit import Vector

from . import xyz
from .lab import (
    from_bsh,
    from_lch,
    from_xyz,
    from_xyz_lum,
    to_bsh,
    to_lch,
    to_xyz,
    to_xyz_lum,
)
from .space import SRGB


class LabTest(LinalgTestCase):
    def test_from_xyz(self) -> None:
        def rgb_to_lab(color: Vector) -> Vector:
            return from_xyz(xyz.from_rgb(color, SRGB))

        self.assert_vector_equal([0.0, 0.0, 0.0], rgb_to_lab([0.0, 0.0, 0.0]))
        self.assert_vector_equal(
            [100.0000014, -7.8e-06, 6.8e-06], rgb_to_lab([1.0, 1.0, 1.0])
        )
        self.assert_vector_equal(
            [51.5430656, -3.6629291, -47.2441356],
            rgb_to_lab([0.2, 0.5, 0.8]),
        )

    def test_to_xyz(self) -> None:
        def lab_to_rgb(color: Vector) -> Vector:
            return xyz.to_rgb(to_xyz(color), SRGB)

        self.assert_vector_equal([0.0, 0.0, 0.0], lab_to_rgb([0.0, 0.0, 0.0]))
        self.assert_vector_equal(
            [1.7344583, 0.5737799, 0.2085584], lab_to_rgb([100.0, 100.0, 100.0])
        )
        self.assert_vector_equal(
            [0.5491071, 0.4599878, -0.51266], lab_to_rgb([50.0, 0.0, 100.0])
        )
        self.assert_vector_equal(
            [1.0006989, -0.9189066, 0.4878331], lab_to_rgb([50.0, 100.0, 0.0])
        )

    def test_to_lch(self) -> None:
        self.assert_vector_equal([0.0, 0.0, 0.0], to_lch([0.0, 0.0, 0.0]))
        self.assert_vector_equal(
            [100.0, 141.4213562, 45.0], to_lch([100.0, 100.0, 100.0])
        )
        self.assert_vector_equal([50.0, 25.0, 90.0], to_lch([50.0, 0.0, 25.0]))
        self.assert_vector_equal([32.0, 25.0, 270.0], to_lch([32.0, 0.0, -25.0]))
        self.assert_vector_equal(
            [50.0, 22.3606798, 63.4349488], to_lch([50.0, 10.0, 20.0])
        )
        self.assert_vector_equal(
            [50.0, 22.3606798, 153.4349488], to_lch([50.0, -20.0, 10.0])
        )
        self.assert_vector_equal(
            [50.0, 20.6155281, 194.0362435], to_lch([50.0, -20.0, -5.0])
        )

    def test_from_lch(self) -> None:
        self.assert_vector_equal([0.0, 0.0, 0.0], from_lch([0.0, 0.0, 0.0]))
        self.assert_vector_equal([100.0, 100.0, 0.0], from_lch([100.0, 100.0, 360.0]))
        self.assert_vector_equal(
            [50.0, 45.6772729, 20.3368322], from_lch([50.0, 50.0, 24.0])
        )
        self.assert_vector_equal([75.0, 0.0, -1], from_lch([75.0, 1.0, 270.0]))

    def test_to_bsh(self) -> None:
        self.assert_vector_equal(to_bsh([0, 0, 0]), [0, 0, 0])
        self.assert_vector_equal(to_bsh([0, 100, 100]), [141.4213562, 100, 45])
        self.assert_vector_equal(to_bsh([100, 0, 0]), [100, 0, 0])
        self.assert_vector_equal(to_bsh([100, 100, 0]), [141.4213562, 50, 0])
        self.assert_vector_equal(to_bsh([100, 0, 100]), [141.4213562, 50, 90])

    def test_from_bsh(self) -> None:
        self.assert_vector_equal(from_bsh(to_bsh([0, 0, 0])), [0, 0, 0])
        self.assert_vector_equal(from_bsh(to_bsh([0, 100, 100])), [0, 100, 100])
        self.assert_vector_equal(from_bsh(to_bsh([100, 0, 0])), [100, 0, 0])
        self.assert_vector_equal(from_bsh(to_bsh([100, 100, 0])), [100, 100, 0])
        self.assert_vector_equal(from_bsh(to_bsh([100, 0, 100])), [100, 0, 100])

    def test_xyz_lum(self) -> None:
        self.assertEqual(from_xyz_lum(to_xyz_lum(50)), 50)
