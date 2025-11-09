import math
from typing import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    slope = profile_params.tone.curve.sigmoid.slope
    if exclude_default and not slope.is_set:
        return {}

    contrast_level = round(100 * math.log(slope.value, 32))
    is_enabled = contrast_level > 0

    return {
        "WaveletEnabled": str(is_enabled).lower(),
        "WaveletContrast1": str(contrast_level),
        "WaveletContrast2": str(contrast_level),
    }
