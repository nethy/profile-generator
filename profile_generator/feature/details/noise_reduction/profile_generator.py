from collections.abc import Mapping
from typing import cast

from profile_generator.main.profile_params import NoiseReductionMode, ProfileParams


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    noise_reduction = profile_params.details.noise_reduction
    mode = cast(NoiseReductionMode, noise_reduction.mode.value)
    luminance = noise_reduction.luminance.value
    detail = noise_reduction.detail.value
    chrominance = noise_reduction.chrominance.value
    denoise_enabled = luminance > 0 or chrominance > 0
    impulse_denoise_enabled = mode == NoiseReductionMode.AGGRESSIVE
    return {
        "DenoiseEnabled": str(denoise_enabled).lower(),
        "DenoiseSMethod": mode.value,
        "DenoiseLuma": str(luminance),
        "DenoiseDetail": str(detail),
        "DenoiseChroma": str(chrominance),
        "ImpulseDenoiseEnabled": str(impulse_denoise_enabled).lower(),
    }
