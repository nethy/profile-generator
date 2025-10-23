from typing import Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee

from . import contrast_sigmoid


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    linear_grey18 = profile_params.tone.curve.sigmoid.linear_grey18.value
    slope = profile_params.tone.curve.sigmoid.slope.value
    tone_curve = contrast_sigmoid.get_tone_curve(linear_grey18, slope)
    return {
        "Curve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, tone_curve
        ),
    }
