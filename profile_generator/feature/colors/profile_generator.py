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
    slope = profile_params.tone.curve.sigmoid.slope.value
    gain = profile_params.colors.vibrance.value
    base = 1 / math.pow(slope, 0.618)
    vibrance = base * (1 + gain / _MAX_VIBRANCE)
    chromaticity = (
        min(100 * (vibrance - 1) / 3, 100) if vibrance > 1 else (vibrance - 1) * 100
    )
    is_enabled = not math.isclose(vibrance, 0, rel_tol=1e-2)
    return {
        "ColorAppEnabled": str(is_enabled).lower(),
        "ColorAppChroma": str(round(chromaticity, 1)),
    }
