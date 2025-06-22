from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import curve

from . import lch, matte, toning_regions


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    matte_curve = matte.get_matte_curve(profile_params.colors.grading.matte)

    matte_points = curve.as_points(matte_curve)
    black = profile_params.colors.grading.matte.black.value
    white = profile_params.colors.grading.matte.white.value
    is_enabled = black > 0 and white > 0
    return {
        "RGBCurvesEnabled": str(is_enabled).lower(),
        "RGBCurvesRCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, matte_points if is_enabled else []
        ),
        "RGBCurvesGCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, matte_points if is_enabled else []
        ),
        "RGBCurvesBCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, matte_points if is_enabled else []
        ),
        **toning_regions.generate(profile_params),
        **lch.generate(profile_params),
    }
