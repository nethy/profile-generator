from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, tuple_of

from .. import contrast_bezier
from . import shim


def _process(data: Any) -> Mapping[str, str]:
    args = shim.get_arguments(data)
    curve = contrast_bezier.calculate(*args)
    return shim.marshal_curve(curve)


SCHEMA = object_of(
    {
        "grey": object_of({"x": range_of(0, 255), "y": range_of(0, 255)}),
        "strength": range_of(0.0, 100.0),
        "weights": tuple_of(range_of(0.0, 5.0), range_of(0.0, 5.0)),
    },
    _process,
)
