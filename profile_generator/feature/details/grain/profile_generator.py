from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    strength = profile_params.details.grain.strength.value
    is_enabled = strength > 0
    return {"GrainEnabled": str(is_enabled).lower(), "GrainStrength": str(strength)}
