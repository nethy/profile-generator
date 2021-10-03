from profile_generator.model.linalg_test import LinalgTestCase

from . import xyz
from .lab import from_lch, from_xyz, to_lch, to_xyz
from .space import SRGB


class LabTest(LinalgTestCase):
    def test_from_xyz(self) -> None:
        srgb_to_lab = lambda color: from_xyz(xyz.from_rgb(color, SRGB))
        self.assert_vector_equal([0.0, 0.0, 0.0], srgb_to_lab([0.0, 0.0, 0.0]))
        self.assert_vector_equal(
            [100.0000014, -7.8e-06, 6.8e-06], srgb_to_lab([1.0, 1.0, 1.0])
        )
        self.assert_vector_equal(
            [51.5430656, -3.6629291, -47.2441356],
            srgb_to_lab([0.2, 0.5, 0.8]),
        )

    def test_to_xyz(self) -> None:
        lab_to_srgb = lambda color: xyz.to_rgb(to_xyz(color), SRGB)
        self.assert_vector_equal([0.0, 0.0, 0.0], lab_to_srgb([0.0, 0.0, 0.0]))
        self.assert_vector_equal(
            [1.0, 0.5737799, 0.2085584], lab_to_srgb([100.0, 100.0, 100.0])
        )
        self.assert_vector_equal(
            [0.5491071, 0.4599878, 0.0], lab_to_srgb([50.0, 0.0, 100.0])
        )
        self.assert_vector_equal([1.0, 0.0, 0.4878331], lab_to_srgb([50.0, 100.0, 0.0]))

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
