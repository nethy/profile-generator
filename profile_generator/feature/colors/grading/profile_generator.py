from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import curve

from . import hsv, toning_rgb_curve


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    toning_param = profile_params.colors.grading.toning
    is_enabled = any(
        map(
            lambda param: param.as_list() != [0, 0, 0],
            (
                toning_param.black,
                toning_param.shadow,
                toning_param.midtone,
                toning_param.highlight,
                toning_param.white,
            ),
        )
    )

    if is_enabled:
        toning_curve = toning_rgb_curve.get_rgb_toning(toning_param)
        reds, greens, blues = curve.as_points_multiple(toning_curve)
    else:
        reds = greens = blues = []

    return {
        "RGBCurvesEnabled": str(is_enabled).lower(),
        "RGBCurvesRCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, reds
        ),
        "RGBCurvesGCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, greens
        ),
        "RGBCurvesBCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, blues
        ),
        **hsv.generate(profile_params),
    }
