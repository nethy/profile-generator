from unittest import TestCase

from .colorspace import (
    lab_to_lch,
    lab_to_xyz,
    lch_to_lab,
    rgb_to_srgb,
    rgb_to_xyz,
    srgb_to_rgb,
    xyz_to_lab,
    xyz_to_rgb,
)


class ColorspaceTest(TestCase):
    def test_srgb_to_rgb(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], srgb_to_rgb([0.0, 0.0, 0.0]))
        self._assert_color_equal([1.0, 1.0, 1.0], srgb_to_rgb([1.0, 1.0, 1.0]))
        self._assert_color_equal(
            [0.0015480, 0.2140411, 0.6038273],
            srgb_to_rgb([0.02, 0.5, 0.8]),
        )

    def test_rgb_to_srgb(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], rgb_to_srgb([0.0, 0.0, 0.0]))
        self._assert_color_equal([1.0, 1.0, 1.0], rgb_to_srgb([1.0, 1.0, 1.0]))
        self._assert_color_equal(
            [0.02584, 0.7353570, 0.9063318], rgb_to_srgb([0.002, 0.5, 0.8])
        )

    def test_srgb_to_xyz(self) -> None:
        self._assert_color_equal([0.0, 0.0, 0.0], rgb_to_xyz([0.0, 0.0, 0.0]))
        self._assert_color_equal([0.9504559, 1, 1.0890578], rgb_to_xyz([1.0, 1.0, 1.0]))
        self._assert_color_equal(
            [0.1861554, 0.1969964, 0.5994998],
            rgb_to_xyz(srgb_to_rgb([0.02, 0.5, 0.8])),
        )

    def test_xyz_to_srgb(self) -> None:
        xyz_to_srgb = lambda color: rgb_to_srgb(xyz_to_rgb(color))
        self._assert_color_equal([0.0, 0.0, 0.0], xyz_to_srgb([0.0, 0.0, 0.0]))
        self._assert_color_equal(
            [1.0, 0.9983714, 0.9574252], xyz_to_srgb([0.9504559, 1.0, 1.0])
        )
        self._assert_color_equal(
            [0.0, 0.8949108, 0.8832718], xyz_to_srgb([0.2, 0.5, 0.8])
        )

    def test_srgb_to_lab(self) -> None:
        srgb_to_lab = lambda color: xyz_to_lab(rgb_to_xyz(srgb_to_rgb(color)))
        self._assert_color_equal([0.0, 0.0, 0.0], srgb_to_lab([0.0, 0.0, 0.0]))
        self._assert_color_equal(
            [100.0, -0.0024679, -0.01394372], srgb_to_lab([1.0, 1.0, 1.0])
        )
        self._assert_color_equal(
            [52.2537221, 2.7856434, -46.29965870],
            srgb_to_lab([0.2, 0.5, 0.8]),
        )

    def test_lab_to_srgb(self) -> None:
        lab_to_srgb = lambda color: rgb_to_srgb(xyz_to_rgb(lab_to_xyz(color)))
        self._assert_color_equal(
            [0.0, 0.2517690, 0.7611571], lab_to_srgb([0.0, 0.0, 0.0])
        )
        self._assert_color_equal(
            [1.0, 0.2751861, 0.0], lab_to_srgb([1.0, 255 / 256, 255 / 256])
        )
        self._assert_color_equal(
            [0.0, 0.5979016, 0.0], lab_to_srgb([0.5, 0 / 256, 255 / 256])
        )
        self._assert_color_equal(
            [0.7182831, 0.0, 1.0], lab_to_srgb([0.5, 255 / 256, 0 / 256])
        )

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

    def _assert_color_equal(self, list1: list[float], list2: list[float]) -> None:
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b)
