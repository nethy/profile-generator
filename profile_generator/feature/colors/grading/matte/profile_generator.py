import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import CurveType

from . import matte


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    R_CURVE: Final = "RGBCurvesRCurve"
    G_CURVE: Final = "RGBCurvesGCurve"
    B_CURVE: Final = "RGBCurvesBCurve"


_POINT_COUNT = 32


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    grading_params = profile_params.colors.grading
    lightness_curve = matte.get_lightness_curve(grading_params.toning)
    matte_curve = matte.get_matte_curve(grading_params.matte)

    curve = lambda x: matte_curve(lightness_curve(x))

    refs = (i / (_POINT_COUNT - 1) for i in range(_POINT_COUNT))
    points = [curve(x) for x in refs]
    curve_output = raw_therapee.present_curve(CurveType.STANDARD, points)

    is_enabled = any(not math.isclose(x, y) for x, y in zip(refs, points))
    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.R_CURVE: curve_output,
        Template.B_CURVE: curve_output,
        Template.G_CURVE: curve_output,
    }