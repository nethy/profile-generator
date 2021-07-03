from profile_generator.model.linalg_test import LinalgTestCase

from .rgb import normalize, rgb_to_hsv


class RgbTest(LinalgTestCase):
    def test_noramlize_rgb(self) -> None:
        self.assert_vector_equal(normalize([0, 127, 255]), [0, 0.4980392, 1])

    def test_rgb_to_hsv(self) -> None:
        self.assert_vector_equal(
            rgb_to_hsv(normalize([70, 49, 33])), [0.0720721, 0.5285714, 0.2745098]
        )
