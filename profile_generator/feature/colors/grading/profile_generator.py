from collections.abc import Mapping

from profile_generator.feature.colors.grading import rgb_curve
from profile_generator.main.profile_params import ProfileParams

from . import hsv


def generate(profile_params: ProfileParams, exclude_defult: bool) -> Mapping[str, str]:
    return {
        **rgb_curve.generate(profile_params, exclude_defult),
        **hsv.generate(profile_params, exclude_defult),
    }
