from collections.abc import Mapping
from typing import Callable

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Vector, curve

from . import matte, toning_rgb_curve


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    toning_params = profile_params.colors.grading.toning
    matte_strength = profile_params.colors.grading.matte
    if exclude_default and not toning_params.is_set and not matte_strength.is_set:
        return {}

    toning_curve = toning_rgb_curve.get_rgb_toning(toning_params)
    matte_curve = matte.get_matte_curve(matte_strength.value)

    is_enabled = toning_curve is not None or matte_curve is not None
    toning_curve = toning_curve if toning_curve is not None else lambda x: [x] * 3
    matte_curve = matte_curve if matte_curve is not None else lambda x: x

    def merged_curve(x: float) -> Vector:
        return list(map(matte_curve, toning_curve(x)))

    return _present_rgb_curve(is_enabled, merged_curve)


def _present_rgb_curve(
    is_enabled: bool, rgb_curve: Callable[[float], Vector]
) -> Mapping[str, str]:
    reds, greens, blues = curve.as_points_multiple(rgb_curve)
    return {
        "RGBCurvesEnabled": str(is_enabled).lower(),
        "RGBCurvesRCurve": (
            raw_therapee.present_curve(raw_therapee.CurveType.FLEXIBLE, reds)
            if is_enabled
            else raw_therapee.present_linear_curve()
        ),
        "RGBCurvesGCurve": (
            raw_therapee.present_curve(raw_therapee.CurveType.FLEXIBLE, greens)
            if is_enabled
            else raw_therapee.present_linear_curve()
        ),
        "RGBCurvesBCurve": (
            raw_therapee.present_curve(raw_therapee.CurveType.FLEXIBLE, blues)
            if is_enabled
            else raw_therapee.present_linear_curve()
        ),
    }
