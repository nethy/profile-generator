from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams


class Template:
    METHOD: Final = "BayerMethod"
    AUTO_CONTRAST: Final = "BayerDDAutoContrast"
    CONTRAST: Final = "BayerDDContrast"


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    demosaic = profile_params.raw.demosaic
    return {
        Template.METHOD: demosaic.algorithm.value.value.lower(),
        Template.AUTO_CONTRAST: str(demosaic.auto_threshold.value).lower(),
        Template.CONTRAST: str(demosaic.threshold.value),
    }
