from profile_generator.model.linalg_test import LinalgTestCase

from .rgb import clip_linear, from_hsv, normalize, to_hsv


class RgbTest(LinalgTestCase):
    def test_noramlize(self) -> None:
        self.assert_vector_equal(normalize([0, 127, 255]), [0, 0.4980392, 1])

    def test_to_hsv(self) -> None:
        self.assert_vector_equal(
            to_hsv(normalize([70, 49, 33])), [0.0720721, 0.5285714, 0.2745098]
        )

    def test_from_hsv(self) -> None:
        self.assert_vector_equal(
            from_hsv([0.0833333, 0.38, 0.62]), [0.62, 0.5022, 0.3844]
        )
        self.assert_vector_equal(
            from_hsv(to_hsv(normalize([70, 49, 33]))), normalize([70, 49, 33])
        )

    def test_clip_linear(self) -> None:
        self.assert_vector_equal(clip_linear([1.1, 1.3, 1.2]), [1.0, 1.0, 1.0])
        self.assert_vector_equal(
            clip_linear([0.8, 0.5, 1.1]), [0.760864, 0.5217281, 1.0]
        )
        self.assert_vector_equal(
            clip_linear([0.2, 0.3, -0.1]), [0.2142529, 0.2856705, 0.0]
        )
        self.assert_vector_equal(clip_linear([-0.1, -0.3, -0.2]), [0.0, 0.0, 0.0])
