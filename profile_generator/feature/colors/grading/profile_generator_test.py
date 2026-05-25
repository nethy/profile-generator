from profile_generator.feature.colors.grading import hsv_test

DEFAULT = {
    "RGBCurvesEnabled": "false",
    "RGBCurvesRCurve": "0;",
    "RGBCurvesGCurve": "0;",
    "RGBCurvesBCurve": "0;",
    **hsv_test.DEFAULT,
}
