from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.unit.precision import DECIMALS

from .grading.profile_generator import generate as generate_grading
from .space.profile_generator import generate as generate_space
from .white_balance.profile_generator import generate as generate_white_balance


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **_get_vibrance(profile_params),
        **generate_grading(profile_params),
        **generate_space(profile_params),
        **generate_white_balance(profile_params)
    }


_MAX_VIBRANCE: Final = 10
_COEFFICIENT: Final = 100 / 3


def _get_vibrance(profile_params: ProfileParams) -> Mapping[str, str]:
    vibrance = profile_params.colors.vibrance.value
    chromaticity = vibrance / _MAX_VIBRANCE * _COEFFICIENT
    is_enabled = chromaticity != 0.0
    return {
        "ColorAppEnabled": str(is_enabled).lower(),
        "ColorAppChroma": str(round(chromaticity, DECIMALS)),
    }
