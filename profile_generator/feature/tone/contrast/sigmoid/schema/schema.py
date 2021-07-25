from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, tuple_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, gamma, hl_tone, gain, offsets = shim.get_parameters(data)
    points = contrast_sigmoid.calculate(grey, gamma, hl_tone, gain, offsets)
    return shim.marshal_curve(points)


_MIDDLE_GREY_RGB = range_of(16.0, 240.0)

SCHEMA = object_of(
    {
        "neutral5": tuple_of(_MIDDLE_GREY_RGB, _MIDDLE_GREY_RGB, _MIDDLE_GREY_RGB),
        "exposure_compensation": range_of(-2.0, 2.0),
        "gamma": range_of(1.0, 5.0),
        "highlight_tone": range_of(-1.0, 1.0),
        "matte_effect": type_of(bool),
    },
    _process,
)
