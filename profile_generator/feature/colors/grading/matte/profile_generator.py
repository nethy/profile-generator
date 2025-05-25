import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import CurveType
from profile_generator.unit import Point

from . import matte


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    R_CURVE: Final = "RGBCurvesRCurve"
    G_CURVE: Final = "RGBCurvesGCurve"
    B_CURVE: Final = "RGBCurvesBCurve"


_POINT_COUNT = 32


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    grading_params = profile_params.colors.grading
    curve = matte.get_matte_curve(grading_params.matte)

    refs = (i / (_POINT_COUNT - 1) for i in range(_POINT_COUNT))
    points = [Point(x, curve(x)) for x in refs]
    curve_output = raw_therapee.present_curve(CurveType.STANDARD, points)

    is_enabled = any(not math.isclose(x, y, rel_tol=1e-7) for x, y in points)
    if not is_enabled:
        curve_output = CurveType.LINEAR
    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.R_CURVE: curve_output,
        Template.B_CURVE: curve_output,
        Template.G_CURVE: curve_output,
    }
