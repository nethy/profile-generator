from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

from .. import contrast_sigmoid
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    parameters = shim.get_parameters(data)
    tone_curve = contrast_sigmoid.calculate(*parameters)
    return shim.marshal(*tone_curve)


SCHEMA = object_of(
    {
        "grey18": range_of(16.0, 240.0),
        "slope": range_of(1.0, 5.0),
    },
    _process,
)
