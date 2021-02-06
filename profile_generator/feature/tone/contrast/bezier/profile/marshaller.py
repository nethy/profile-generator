from typing import Any, Dict

from .. import contrast_bezier
from . import shim


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    args = shim.get_arguments(configuration)
    curve = contrast_bezier.calculate(*args)
    return shim.marshal_curve(curve)
