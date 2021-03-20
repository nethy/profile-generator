from typing import Any, Dict

_ENABLED_FIELD = "WaveletEnabled"
_CURVE_FIELD = "OpacityCurveWL"

_LINEAR_CURVE = "0;"
_CURVE_TEMPLATE = "1;0;0.5;0;0.16667;0.5;{:.5f};0.33333;0.3333333;1;0.5;0.166667;0;"


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    local = configuration.get("local", 0)
    is_enabled = False
    curve = _LINEAR_CURVE
    if local > 0:
        is_enabled = True
        curve = _CURVE_TEMPLATE.format(0.5 * (1 + local / 100))
    return {_ENABLED_FIELD: str(is_enabled).lower(), _CURVE_FIELD: curve}
