from typing import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {"CMWorkingProfile": profile_params.colors.profile.working.value.value}

