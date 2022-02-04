from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    grey, slope = shim.get_parameters(data)
    curve = contrast_sigmoid.calculate(grey, slope)
    return shim.marshal(curve)


SCHEMA = object_of(
    {
        "grey18": range_of(16.0, 240.0),
        "slope": range_of(1.0, 5.0),
    },
    _process,
)
