import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams

from .grading.profile_generator import generate as generate_grading
from .hsl.profile_generator import generate as generate_hsl
from .space.profile_generator import generate as generate_space
from .white_balance.profile_generator import generate as generate_white_balance


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **_get_vibrance(profile_params),
        **generate_grading(profile_params),
        **generate_hsl(profile_params),
        **generate_space(profile_params),
        **generate_white_balance(profile_params),
    }


class Template:
    CHROMATICITY: Final = "LcChromaticity"


_MAX_VIBRANCE: Final = 10.0
_CONTRAST_VIBRANCE_EXPONENT = 0.605


def _get_vibrance(profile_params: ProfileParams) -> Mapping[str, str]:
    contrast = profile_params.tone.curve.sigmoid.slope.value
    vibrance = profile_params.colors.vibrance.value
    base = math.pow(contrast, _CONTRAST_VIBRANCE_EXPONENT)
    multiplier = math.sqrt(1 + (vibrance / _MAX_VIBRANCE))
    chromaticity = _get_chromaticity(base * multiplier)
    return {Template.CHROMATICITY: str(chromaticity)}


def _get_chromaticity(value: float) -> int:
    return min(100, round((value - 1) * 100))
