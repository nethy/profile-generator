"""
RawTherapee CIECAM chromaticity, saturation, colorfulness function

f(x) = (1-p/100) * x + p/100 * (1-(1-x)^4))

f'(x) = 1-p/100 + p/100 * 4(1-x)^3
f'(0) = 1-p/100 + 4p/100 = 1 + 3p/100

p = 100*(f'(0)-1)/3
"""

import math
from collections.abc import Mapping
from functools import cache
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model import gamma
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Curve, curve

from .grading.profile_generator import generate as generate_grading
from .white_balance.profile_generator import generate as generate_white_balance


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    return {
        **_get_vibrance(profile_params, exclude_default),
        **generate_grading(profile_params, exclude_default),
        **generate_white_balance(profile_params, exclude_default),
    }


_MAX_VIBRANCE: Final = 10
_WEIGHT_TRESHOLD = 0.5


def _get_vibrance(
    profile_params: ProfileParams, exclude_default: bool
) -> Mapping[str, str]:
    vibrance_params = profile_params.colors.vibrance
    if exclude_default and not vibrance_params.is_set:
        return {}

    gain = vibrance_params.value
    vibrance = 1.0 + gain / _MAX_VIBRANCE
    is_vibrance_enabled = vibrance > 1.0
    cc_curve = _get_cc_curve(vibrance)
    cc_points = (
        raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, curve.as_points(cc_curve)
        )
        if is_vibrance_enabled
        else raw_therapee.CurveType.LINEAR
    )

    power = 1 + profile_params.colors.color_chrome.value / 10
    saturation = (1 / power - 1) * 100
    is_color_chrome_enabled = power > 1
    return {
        "LCEnabled": str(is_vibrance_enabled).lower(),
        "CCCurve": cc_points,
        "CTEnabled": str(is_color_chrome_enabled).lower(),
        "CTPower": str(power),
        "CTSaturation": str(round(saturation)),
    }


@cache
def _get_cc_curve(vibrance: float) -> Curve:
    cc_base_curve = gamma.reciprocal(vibrance)

    def weight(x: float) -> float:
        if x < _WEIGHT_TRESHOLD:
            return 0.5 * math.pow(1 - x / _WEIGHT_TRESHOLD, 2)
        else:
            return 0

    def cc_curve(x: float) -> float:
        w = weight(x)
        return w * x + (1 - w) * cc_base_curve(x)

    return cc_curve
