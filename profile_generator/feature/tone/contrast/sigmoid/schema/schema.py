from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, tuple_of, type_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, gamma, gain, offsets = shim.get_parameters(data)
    points = contrast_sigmoid.calculate(grey, gamma, gain, offsets)
    return shim.marshal_curve(points)


_GAIN_RANGE = range_of(1.0, 4.0)

SCHEMA = object_of(
    {
        "neutral5": tuple_of(range_of(16, 240), range_of(16, 240), range_of(16, 240)),
        "exposure_compensation": range_of(-2.0, 2.0),
        "gamma": range_of(1.0, 5.0),
        "gain": object_of({"shadow": _GAIN_RANGE, "highlight": _GAIN_RANGE}),
        "matte_effect": type_of(bool),
    },
    _process,
)
