from typing import Any

from profile_generator.functions import equalizer
from profile_generator.unit import Point

_ENABLED_FIELD = "WaveletEnabled"
_CURVE_FIELD = "OpacityCurveWL"

_LINEAR_CURVE = "0;"


def get_profile_args(configuration: dict[str, Any]) -> dict[str, str]:
    local = configuration.get("local", 0)
    is_enabled = False
    raw_curve = _LINEAR_CURVE
    if local > 0:
        is_enabled = True
        y = 0.5 * (1 + local / 100)
        curve = equalizer.equalize(
            Point(0, 0.5), Point(0.4, y), Point(0.6, y), Point(1, 0.5)
        )
        raw_curve = "1;" + "".join([p.for_raw_therapee() for p in curve])
    return {_ENABLED_FIELD: str(is_enabled).lower(), _CURVE_FIELD: raw_curve}
