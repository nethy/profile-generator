from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, gamma, hl_protection, ev_comp, offsets = shim.get_parameters(data)
    curve = contrast_sigmoid.calculate(grey, gamma, offsets, hl_protection, ev_comp)
    return shim.marshal_curve(curve)


SCHEMA = object_of(
    {
        "grey18": range_of(16.0, 240.0),
        "gamma": range_of(1.0, 5.0),
        "highlight_protection": type_of(bool),
        "exposure_compensation": range_of(-2.0, 2.0),
        "matte_effect": type_of(bool),
    },
    _process,
)
