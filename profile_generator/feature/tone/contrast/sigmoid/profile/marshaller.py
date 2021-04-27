from typing import Any

from .. import contrast_sigmoid
from . import shim

_SAMPLE_SIZE = 17


def get_profile_args(configuration: dict[str, Any]) -> dict[str, str]:
    grey, strength = shim.get_parameters(configuration)
    points = contrast_sigmoid.calculate(grey, strength, _SAMPLE_SIZE)
    return shim.marshal_curve(points)
