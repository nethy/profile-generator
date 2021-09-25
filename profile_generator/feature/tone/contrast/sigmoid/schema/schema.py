from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of, range_of

from .. import contrast_sigmoid
from . import shim
from .highlight import Highlight


def _process(data: Any) -> Mapping[str, str]:
    grey, slope, brightness, highlight = shim.get_parameters(data)
    curve = contrast_sigmoid.calculate(grey, slope, brightness, highlight)
    return shim.marshal_curve(curve)


SCHEMA = object_of(
    {
        "grey18": range_of(16.0, 240.0),
        "slope": range_of(1.0, 5.0),
        "brightness": range_of(-2.0, 2.0),
        "highlight": options_of(*[option.name.lower() for option in Highlight]),
    },
    _process,
)
