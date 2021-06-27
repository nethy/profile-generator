from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, tuple_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, gamma, hlp, offsets = shim.get_parameters(data)
    points = contrast_sigmoid.calculate(grey, gamma, hlp, offsets)
    return shim.marshal_curve(points)


SCHEMA = object_of(
    {
        "neutral5": tuple_of(range_of(16, 240), range_of(16, 240), range_of(16, 240)),
        "exposure_compensation": range_of(-2.0, 2.0),
        "gamma": range_of(1.0, 5.0),
        "highlight_protection": range_of(1.0, 4.0),
        "matte_effect": type_of(bool),
    },
    _process,
)
