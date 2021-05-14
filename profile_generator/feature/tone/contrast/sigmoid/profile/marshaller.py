from collections.abc import Mapping
from typing import Any

from .. import contrast_sigmoid
from . import shim


def get_profile_args(configuration: Mapping[str, Any]) -> Mapping[str, str]:
    grey, strength, protect_hl, offsets = shim.get_parameters(configuration)
    if protect_hl:
        points = contrast_sigmoid.calculate_with_hl_protection(grey, strength, offsets)
    else:
        points = contrast_sigmoid.calculate(grey, strength, offsets)
    return shim.marshal_curve(points)
