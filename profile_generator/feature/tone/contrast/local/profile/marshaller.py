from typing import Any

from profile_generator.functions import equalizer
from profile_generator.unit import Point

_ENABLED_FIELD = "WaveletEnabled"
_CURVE_FIELD = "OpacityCurveWL"

_LINEAR_CURVE = "0;"
_CURVE_TEMPLATE = (
    "1;0;0.5;0;0.25;0.4;{value:.5f};0.25;0;0.6;{value:.5f};0;0.25;1;0.5;0.25;0;"
)


def get_profile_args(configuration: dict[str, Any]) -> dict[str, str]:
    local = configuration.get("local", 0)
    is_enabled = False
    curve = _LINEAR_CURVE
    if local > 0:
        is_enabled = True
        y = 0.5 * (1 + local / 100)
        curve = equalizer.to_raw_therapee(
            Point(0, 0.5), Point(0.4, y), Point(0.6, y), Point(1, 0.5)
        )
    return {_ENABLED_FIELD: str(is_enabled).lower(), _CURVE_FIELD: curve}
