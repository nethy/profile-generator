from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams

from . import hsv, matte, toning_rgb_curve


def generate(profile_params: ProfileParams, exclude_defult: bool) -> Mapping[str, str]:
    return {
        **toning_rgb_curve.generate(profile_params, exclude_defult),
        **hsv.generate(profile_params, exclude_defult),
        **matte.generate(profile_params, exclude_defult),
    }
