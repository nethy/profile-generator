from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams

from .grain.profile_generator import generate as grain
from .noise_reduction.profile_generator import generate as noise_reduction
from .sharpening.capture.profile_generator import generate as capture_sharpening
from .sharpening.output.profile_generator import generate as output_sharpening


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    return {
        **grain(profile_params, exclude_default),
        **noise_reduction(profile_params, exclude_default),
        **capture_sharpening(profile_params, exclude_default),
        **output_sharpening(profile_params, exclude_default),
    }
