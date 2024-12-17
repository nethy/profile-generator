import math
from typing import Final, Mapping

from profile_generator.main.profile_params import ProfileParams


class Template:
    ENABLED: Final = "WaveletEnabled"
    CONSTRAST_1: Final = "WaveletContrast1"
    CONSTRAST_2: Final = "WaveletContrast2"


_BASE_SLOPE = 1.5


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    slope = profile_params.tone.curve.sigmoid.slope.value * _BASE_SLOPE

    contrast_level = round(100 * math.log(slope, 8))
    is_enabled = contrast_level > 0

    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.CONSTRAST_1: str(contrast_level),
        Template.CONSTRAST_2: str(contrast_level),
    }
