from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams

from .matte import generate as generate_matte
from .toning import generate as generate_toning


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **generate_toning(profile_params),
        **generate_matte(profile_params),
    }
