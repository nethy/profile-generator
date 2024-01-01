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
        **_get_vibrance(profile_params.colors.vibrance.value),
        **generate_grading(profile_params),
        **generate_hsl(profile_params),
        **generate_space(profile_params),
        **generate_white_balance(profile_params),
    }

class Template:
    VIBRANCE_ENABLED: Final = "VibranceEnabled"
    VIBRANCE_PASTELS: Final = "VibrancePastels"
    VIBRANCE_SATURATED: Final = "VibranceSaturated"
    HSV_ENABLED: Final = "HsvEnabled"
    S_CURVE: Final = "HsvSCurve"

_MAX_VIBRANCE: Final = 10

def _get_vibrance(vibrance: float) -> Mapping[str, str]:
    multiplier = math.sqrt(1 + vibrance / _MAX_VIBRANCE)
    return __get_vibrance(multiplier) | _get_hsv(multiplier)

def __get_vibrance(multiplier: float) -> Mapping[str, str]:
    pastels = round(100 * (multiplier - 1))
    saturated = round(pastels / 2)
    return {
        Template.VIBRANCE_ENABLED: str(multiplier > 1).lower(),
        Template.VIBRANCE_PASTELS: str(pastels),
        Template.VIBRANCE_SATURATED: str(saturated),
    }

def _get_hsv(multiplier: float) -> Mapping[str, str]:
    base = 0.5 * multiplier
    skin = 0.5 * ((multiplier - 1) * 0.5 + 1)
    equalizer = [
        EqPoint(10 / 360, skin),
        EqPoint(40 / 360, skin),
        EqPoint(70 / 360, base),
        EqPoint(340 / 360, base),
    ]
    return {
        Template.HSV_ENABLED: str(multiplier > 1).lower(),
        Template.S_CURVE: raw_therapee.present_equalizer(equalizer)
    }