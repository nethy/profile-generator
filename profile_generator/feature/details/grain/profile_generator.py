from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    strength_param = profile_params.details.grain.strength
    if exclude_default and not strength_param.is_set:
        return {}

    strength = strength_param.value
    is_enabled = strength > 0
    return {"GrainEnabled": str(is_enabled).lower(), "GrainStrength": str(strength)}
