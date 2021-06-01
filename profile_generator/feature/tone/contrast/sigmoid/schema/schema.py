from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, strength, protect_hl, offsets = shim.get_parameters(data)
    if protect_hl:
        points = contrast_sigmoid.calculate_with_hl_protection(grey, strength, offsets)
    else:
        points = contrast_sigmoid.calculate(grey, strength, offsets)
    return shim.marshal_curve(points)


SCHEMA = object_of(
    {
        "grey": object_of({"x": range_of(16, 240), "y": range_of(64, 192)}),
        "strength": range_of(0.0, 100.0),
        "protect_hl": type_of(bool),
        "matte_effect": type_of(bool),
    },
    _process,
)
