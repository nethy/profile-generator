from . import xyz
from .colorspacetest import ColorspaceTest
from .lab import lab_to_lch, lab_to_xyz, lch_to_lab, xyz_to_lab


class LabTest(ColorspaceTest):
    def test_srgb_to_lab(self) -> None:
        srgb_to_lab = lambda color: xyz_to_lab(xyz.srgb_to_xyz(color))
        self.assert_color_equal([0.0, 0.0, 0.0], srgb_to_lab([0.0, 0.0, 0.0]))
        self.assert_color_equal([100.0, 0.0, 0.0], srgb_to_lab([1.0, 1.0, 1.0]))
        self.assert_color_equal(
            [52.2522841, 2.7790458, -46.2895491],
            srgb_to_lab([0.2, 0.5, 0.8]),
        )

    def test_lab_to_srgb(self) -> None:
        lab_to_srgb = lambda color: xyz.xyz_to_srgb(lab_to_xyz(color))
        self.assert_color_equal([0.0, 0.0, 0.0], lab_to_srgb([0.0, 0.0, 0.0]))
        self.assert_color_equal(
            [1.0, 0.5746288, 0.1939663], lab_to_srgb([100.0, 100.0, 100.0])
        )
        self.assert_color_equal(
            [0.5739409, 0.4558792, 0.0], lab_to_srgb([50.0, 0.0, 100.0])
        )
        self.assert_color_equal([1.0, 0.0, 0.4828316], lab_to_srgb([50.0, 100.0, 0.0]))

    def test_lab_to_lch(self) -> None:
        self.assert_color_equal([0.0, 0.0, 0.0], lab_to_lch([0.0, 0.0, 0.0]))
        self.assert_color_equal(
            [100.0, 141.4213562, 45.0], lab_to_lch([100.0, 100.0, 100.0])
        )
        self.assert_color_equal([50.0, 25.0, 90.0], lab_to_lch([50.0, 0.0, 25.0]))
        self.assert_color_equal([32.0, 25.0, 270.0], lab_to_lch([32.0, 0.0, -25.0]))
        self.assert_color_equal(
            [50.0, 22.3606798, 63.4349488], lab_to_lch([50.0, 10.0, 20.0])
        )
        self.assert_color_equal(
            [50.0, 22.3606798, 153.4349488], lab_to_lch([50.0, -20.0, 10.0])
        )
        self.assert_color_equal(
            [50.0, 20.6155281, 194.0362435], lab_to_lch([50.0, -20.0, -5.0])
        )

    def test_lch_to_lab(self) -> None:
        self.assert_color_equal([0.0, 0.0, 0.0], lch_to_lab([0.0, 0.0, 0.0]))
        self.assert_color_equal([100.0, 100.0, 0.0], lch_to_lab([100.0, 100.0, 360.0]))
        self.assert_color_equal(
            [50.0, 45.6772729, 20.3368322], lch_to_lab([50.0, 50.0, 24.0])
        )
        self.assert_color_equal([75.0, 0.0, -1], lch_to_lab([75.0, 1.0, 270.0]))
