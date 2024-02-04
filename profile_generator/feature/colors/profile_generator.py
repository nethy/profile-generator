import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint

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
    VIBRANCE_ENABLED: Final = "VibranceEnabled"
    VIBRANCE_PASTELS: Final = "VibrancePastels"
    VIBRANCE_SATURATED: Final = "VibranceSaturated"
    CT_ENABLED: Final = "ColorToningEnabled"
    CT_SATURATION: Final = "ColorToningSaturation"


_MAX_VIBRANCE: Final = 10


def _get_vibrance(profile_params: ProfileParams) -> Mapping[str, str]:
    vibrance = profile_params.colors.vibrance.value
    contrast = profile_params.tone.curve.sigmoid.slope.value
    base = math.pow(contrast, 0.605)
    multiplier = 1 + vibrance / _MAX_VIBRANCE
    value = math.sqrt(base * multiplier)
    vibrance = _as_interval(value)
    saturation = _as_interval(value) / 2
    return {
        Template.VIBRANCE_ENABLED: str(vibrance > 1).lower(),
        Template.VIBRANCE_PASTELS: str(round(vibrance)),
        Template.VIBRANCE_SATURATED: str(round(vibrance / 2)),
        Template.CT_ENABLED: str(saturation > 1).lower(),
        Template.CT_SATURATION: str(round(saturation))
    }

def _as_interval(value: float) -> float:
    return 100 * (value - 1)
