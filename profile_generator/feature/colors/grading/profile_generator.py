from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams

from .toning import generate as generate_toning


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **generate_toning(profile_params),
    }
