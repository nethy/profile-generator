from profile_generator.main.profile_params import ColorToning
from profile_generator.model.linalg_test import LinalgTestCase

from .toning import get_lab_toning


class ToningTest(LinalgTestCase):
    def test_get_lab_curve_empty(self) -> None:
        params = ColorToning()
        params.parse({})
        curve = get_lab_toning(params)

        self.assertEqual(curve(0), [0, 0, 0])
        self.assertEqual(curve(100), [100, 0, 0])

    def test_get_lab_curve_channels_two(self) -> None:
        params = ColorToning()
        params.parse(
            {
                "channels": "two",
                "black": [1, 1, 30],
                "shadow": [2, 2, 90],
                "highlight": [-1, 2, 180],
                "white": [-2, 3, 270],
            }
        )
        curve = get_lab_toning(params)

        self.assert_vector_equal(curve(0.0000000), [1.0, 0.8660254, 0.5])
        self.assert_vector_equal(curve(33.333333), [35.333333, 0.0, 2.0])
        self.assert_vector_equal(curve(66.666667), [65.666667, -2.0, -0.0])
        self.assert_vector_equal(curve(100.00000), [98.0, 0.0, -3.0])

    def test_get_lab_curve_cinematic(self) -> None:
        params = ColorToning()
        params.parse(
            {
                "channels": "two",
                "shadow": [0, 20, 270],
                "highlight": [0, 20, 90],
            }
        )
        curve = get_lab_toning(params)

        self.assert_vector_equal(curve(0.0000000), [0, 0, 0])
        self.assert_vector_equal(curve(33.333333), [33.333333, -0.0, -20.0])
        self.assert_vector_equal(curve(66.666667), [66.666667, 0.0, 20.0])
        self.assert_vector_equal(curve(100.00000), [100, 0, 0])
