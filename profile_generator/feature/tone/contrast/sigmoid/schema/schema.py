from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, gamma, ev_comp, offsets = shim.get_parameters(data)
    contrast = contrast_sigmoid.calculate(grey, gamma, offsets)
    controls = contrast_sigmoid.base_controls(grey, ev_comp)
    return shim.marshal_curves(controls, contrast)


SCHEMA = object_of(
    {
        "neutral5": range_of(16.0, 240.0),
        "exposure_compensation": range_of(-2.0, 2.0),
        "gamma": range_of(1.0, 5.0),
        "matte_effect": type_of(bool),
    },
    _process,
)
