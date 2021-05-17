from collections.abc import Mapping
from typing import Any

from .. import contrast_bezier
from . import shim


def get_profile_args(configuration: Mapping[str, Any]) -> Mapping[str, str]:
    args = shim.get_arguments(configuration)
    curve = contrast_bezier.calculate(*args)
    return shim.marshal_curve(curve)
