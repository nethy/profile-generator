from unittest import TestCase

from profile_generator.main.profile_params import ColorTone

from .toning import get_lab_mapping


class ToningTest(TestCase):
    def test_get_lab_curve_empty(self) -> None:
        curve = get_lab_mapping([])

        self.assertEqual(curve(0), [0, 0, 0])
        self.assertEqual(curve(1), [1, 0, 0])

    def test_get_lab_curve_single(self) -> None:
        input = [[0.5, 0, 1, 2]]
        color_tones =

        curve = get_lab_mapping()
