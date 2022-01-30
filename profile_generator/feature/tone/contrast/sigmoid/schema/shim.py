import math
from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_GREY18 = 90.0
_DEFAULT_SLOPE = 1.0

_CURVE = "Curve"
_LC_ENABLED = "LCEnabled"
_CHROMATICITY = "Chromaticity"


def get_parameters(configuration: Mapping[str, Any]) -> tuple[float, float]:
    grey18 = configuration.get("grey18", _DEFAULT_GREY18)
    slope = configuration.get("slope", _DEFAULT_SLOPE)
    return (grey18, slope)


def marshal(slope: float, curve: Sequence[Point]) -> Mapping[str, str]:
    curve_value = raw_therapee.CurveType.LINEAR
    if len(curve) > 0:
        curve_value = raw_therapee.present_curve(raw_therapee.CurveType.STANDARD, curve)
    chromaticity_value = _get_chromacity_compensation(slope)
    result = {
        _CURVE: curve_value,
        _CHROMATICITY: str(round(chromaticity_value)),
    }
    if chromaticity_value != 0:
        result |= {_LC_ENABLED: "true"}
    return result


def _get_chromacity_compensation(slope: float) -> float:
    return (math.pow(1 / slope, 0.25) - 1) * 100
