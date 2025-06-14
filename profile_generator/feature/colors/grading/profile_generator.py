import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Vector
from profile_generator.unit.point import Point

from . import matte, toning


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    RED: Final = "RGBCurvesRCurve"
    GREEN: Final = "RGBCurvesGCurve"
    BLUE: Final = "RGBCurvesBCurve"


_SECTION_COUNT = 32


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    rgb_toning = toning.get_rgb_toning(profile_params.colors.grading.toning)
    matte_curve = matte.get_matte_curve(profile_params.colors.grading.matte)

    def rgb_curve(x: float) -> Vector:
        return list(map(matte_curve, rgb_toning(x)))

    reds, greens, blues = [], [], []
    for x in (i / _SECTION_COUNT for i in range(_SECTION_COUNT + 1)):
        r, g, b = rgb_curve(x)
        reds.append(Point(x, _clip(r, 0, 1)))
        greens.append(Point(x, _clip(g, 0, 1)))
        blues.append(Point(x, _clip(b, 0, 1)))

    is_enabled = any(
        not math.isclose(x, y, rel_tol=1e-3) for x, y in (*reds, *greens, *blues)
    )
    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.RED: raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, reds if is_enabled else []
        ),
        Template.GREEN: raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, greens if is_enabled else []
        ),
        Template.BLUE: raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, blues if is_enabled else []
        ),
    }


def _clip(value: float, low: float, high: float) -> float:
    return min(max(value, low), high)
