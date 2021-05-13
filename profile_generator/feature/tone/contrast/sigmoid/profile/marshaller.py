from typing import Any

from .. import contrast_sigmoid
from . import shim

_SAMPLE_SIZE = 17


def get_profile_args(configuration: dict[str, Any]) -> dict[str, str]:
    grey, strength, protect_hl = shim.get_parameters(configuration)
    if protect_hl:
        points = contrast_sigmoid.calculate_with_hl_protection(
            grey, strength, _SAMPLE_SIZE
        )
    else:
        points = contrast_sigmoid.calculate(grey, strength, _SAMPLE_SIZE)
    return shim.marshal_curve(points)
