from typing import Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.color import constants
from profile_generator.model.view import raw_therapee
from profile_generator.unit.precision import equals

from . import contrast_sigmoid


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    linear_grey18 = profile_params.tone.curve.sigmoid.linear_grey18
    slope = profile_params.tone.curve.sigmoid.slope
    if exclude_default and not linear_grey18.is_set and not slope.is_set:
        return {}

    tone_curve = contrast_sigmoid.get_tone_curve(linear_grey18.value, slope.value)
    return {
        "Curve": (
            raw_therapee.present_curve(raw_therapee.CurveType.FLEXIBLE, tone_curve)
            if not equals(linear_grey18.value, constants.GREY18_LINEAR)
            or not equals(slope.value, 1.0, 1e-2)
            else raw_therapee.present_linear_curve()
        ),
    }
