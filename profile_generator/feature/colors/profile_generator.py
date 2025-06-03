"""
RawTherapee CIECAM chromaticity, saturation, colorfulness function

f(x) = (1-p/100) * x + p/100 * (1-(1-x)^4))

f'(x) = 1-p/100 + p/100 * 4(1-x)^3
f'(0) = 1-p/100 + 4p/100 = 1 + 3p/100

p = 100*(f'(0)-1)/3
"""
import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit.point import Point

from .grading.profile_generator import generate as generate_grading
from .space.profile_generator import generate as generate_space
from .white_balance.profile_generator import generate as generate_white_balance


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **_get_vibrance(profile_params),
        **generate_grading(profile_params),
        **generate_space(profile_params),
        **generate_white_balance(profile_params),
    }


_MAX_VIBRANCE: Final = 10


def _get_vibrance(profile_params: ProfileParams) -> Mapping[str, str]:
    gain = profile_params.colors.vibrance.value
    slope = profile_params.tone.curve.sigmoid.slope.value
    vibrance = math.pow(slope, 1 / 2.2) + gain / _MAX_VIBRANCE
    is_enabled = not math.isclose(vibrance, 1, rel_tol=1e-2)
    chroma_curve = (
        [Point(0, 0), Point(0.025, 0.025), Point(1 / vibrance, 1), Point(1, 1)] if is_enabled else []
    )
    return {
        "CCCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.CONTROL_CAGE, chroma_curve
        ),
    }
