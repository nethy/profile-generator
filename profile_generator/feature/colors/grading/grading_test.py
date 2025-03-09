from profile_generator.main.profile_params import ColorGrades, Matte
from profile_generator.model.linalg_test import LinalgTestCase

from .grading import _get_color_grade_lab, _get_matte_rgb


class GradingTest(LinalgTestCase):
    def test_get_color_grade_lab_default(self) -> None:
        grade = _get_color_grade_lab(ColorGrades())
        self.assert_vector_equal(grade(100 / 6), [100 / 6, 0, 0])
        self.assert_vector_equal(grade(50), [50, 0, 0])
        self.assert_vector_equal(grade(100 * 5 / 6), [100 * 5 / 6, 0, 0])

    def test_get_color_grade_lab_colors(self) -> None:
        params = ColorGrades()
        params.parse(
            {
                "shadow_lch": [5, 5, 270],
                "midtone_lch": [0, 0, 0],
                "highlight_lch": [-5, 5, 90],
            }
        )
        grade = _get_color_grade_lab(params)
        self.assert_vector_equal(grade(100 / 6), [100 / 6 + 5, 0, -5])
        self.assert_vector_equal(grade(100 / 3), [100 / 3 + 2.5, 0, -2.5])
        self.assert_vector_equal(grade(50), [50, 0, 0])
        self.assert_vector_equal(grade(100 * 2 / 3), [100 * 2 / 3 - 2.5, 0, 2.5])
        self.assert_vector_equal(grade(100 * 5 / 6), [100 * 5 / 6 - 5, 0, 5])

    def test_get_color_grade_lab_balance(self) -> None:
        params = ColorGrades()
        params.parse(
            {
                "shadow_lch": [5, 5, 270],
                "midtone_lch": [0, 0, 0],
                "highlight_lch": [-5, 5, 90],
                "balance": 0,
            }
        )
        grade = _get_color_grade_lab(params)
        self.assert_vector_equal(grade(100 / 6), [100 / 6 + 5, 0, -5])
        self.assert_vector_equal(
            grade(100 / 3), [100 / 3 + 0.7955179, -0.0, -0.7955179]
        )
        self.assert_vector_equal(grade(50), [50, 0, 0])
        self.assert_vector_equal(
            grade(100 * 2 / 3), [100 * 2 / 3 - 0.7955179, 0, 0.7955179]
        )
        self.assert_vector_equal(grade(100 * 5 / 6), [100 * 5 / 6 - 5, 0, 5])

        params = ColorGrades()
        params.parse(
            {
                "shadow_lch": [5, 5, 270],
                "midtone_lch": [0, 0, 0],
                "highlight_lch": [-5, 5, 90],
                "balance": 100,
            }
        )
        grade = _get_color_grade_lab(params)
        self.assert_vector_equal(grade(100 / 6), [100 / 6 + 5, 0, -5])
        self.assert_vector_equal(grade(100 / 3), [100 / 3 + 4.6875, -0.0, -4.6875])
        self.assert_vector_equal(grade(50), [50, 0, 0])
        self.assert_vector_equal(grade(100 * 2 / 3), [100 * 2 / 3 - 4.6875, 0, 4.6875])
        self.assert_vector_equal(grade(100 * 5 / 6), [100 * 5 / 6 - 5, 0, 5])

    def test_get_color_grade_lab_origo(self) -> None:
        params = ColorGrades()
        params.parse(
            {
                "shadow_lch": [5, 5, 270],
                "midtone_lch": [0, 0, 0],
                "highlight_lch": [-5, 5, 90],
                "origo": 0,
            }
        )
        grade = _get_color_grade_lab(params)
        self.assert_vector_equal(grade(100 / 6 - 50), [0, 0, -5])
        self.assert_vector_equal(grade(100 / 3 - 50), [0, 0, -2.5])
        self.assert_vector_equal(grade(50 - 50), [50 - 50, 0, 0])
        self.assert_vector_equal(
            grade(100 * 2 / 3 - 50), [100 * 2 / 3 - 50 - 2.5, 0, 2.5]
        )
        self.assert_vector_equal(grade(100 * 5 / 6 - 50), [100 * 5 / 6 - 50 - 5, 0, 5])

        params = ColorGrades()
        params.parse(
            {
                "shadow_lch": [5, 5, 270],
                "midtone_lch": [0, 0, 0],
                "highlight_lch": [-5, 5, 90],
                "origo": 100,
            }
        )
        grade = _get_color_grade_lab(params)
        self.assert_vector_equal(grade(100 / 6 + 50), [100 / 6 + 50 + 5, 0, -5])
        self.assert_vector_equal(grade(100 / 3 + 50), [100 / 3 + 50 + 2.5, 0, -2.5])
        self.assert_vector_equal(grade(50 + 50), [50 + 50, 0, 0])
        self.assert_vector_equal(grade(100 * 2 / 3 + 50), [100, 0, 2.5])
        self.assert_vector_equal(grade(100 * 5 / 6 + 50), [100, 0, 5])

    def test_get_matte_rgb(self) -> None:
        params = Matte()
        params.parse({"shadow": 0, "highlight": 255})
        matte = _get_matte_rgb(params)
        self.assertAlmostEqual(matte(0), 0)
        self.assertAlmostEqual(matte(0.05), 0.05)
        self.assertAlmostEqual(matte(0.5), 0.5)
        self.assertAlmostEqual(matte(0.9), 0.9)
        self.assertAlmostEqual(matte(1), 1)

        params = Matte()
        params.parse({"shadow": 10, "highlight": 235})
        matte = _get_matte_rgb(params)
        self.assertAlmostEqual(matte(0), 0.0392157)
        self.assertAlmostEqual(matte(0.05), 0.0551532)
        self.assertAlmostEqual(matte(0.5), 0.5)
        self.assertAlmostEqual(matte(0.9), 0.88969363)
        self.assertAlmostEqual(matte(1), 0.9215686)
