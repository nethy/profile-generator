from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams

from .grain.profile_generator import generate as grain
from .noise_reduction.profile_generator import generate as noise_reduction
from .sharpening.capture.profile_generator import generate as capture_sharpening
from .sharpening.output.profile_generator import generate as output_sharpening


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **grain(profile_params),
        **noise_reduction(profile_params),
        **capture_sharpening(profile_params),
        **output_sharpening(profile_params),
    }
