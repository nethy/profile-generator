from collections.abc import Mapping

import profile_generator.feature.colors.profile_generator as colors
import profile_generator.feature.raw.profile_generator as raw
import profile_generator.feature.tone.contrast.local.profile_generator as local_contrast
from profile_generator.main import ProfileGenerator
from profile_generator.main.profile_params import ProfileParams


def compose_generators(*profile_generators: ProfileGenerator) -> ProfileGenerator:
    def generate(profile_params: ProfileParams) -> Mapping[str, str]:
        return {
            k: v
            for generator in profile_generators
            for k, v in generator(profile_params).items()
        }

    return generate


GENERATOR = compose_generators(colors.generate, raw.generate, local_contrast.generate)
