from typing import Any, Dict

_LAB_ENABLED = "LabEnabled"
_LAB_CHROMATICITY = "LabChromaticity"
_HSV_ENABLED = "HsvEnabled"
_HSV_SCURVE = "HsvSCurve"
_HSV_SCRUVE_TEMPLATE = "1;0;{value:.6f};0;0;1;{value:.6f};0;0;"

_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_CHROMATICITY: "0",
    _HSV_ENABLED: "false",
    _HSV_SCURVE: "0;",
}


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    vibrance = configuration.get("vibrance", 0)
    value = _DEFAULT
    if vibrance > 0:
        value = {**_DEFAULT, **_calculate_hsv_curve(vibrance)}
    elif vibrance < 0:
        value = {**_DEFAULT, **_calculate_chromaticity(vibrance)}
    return value


def _calculate_hsv_curve(vibrance: int) -> Dict[str, str]:
    saturation = 0.5 * (1 + vibrance / 100)
    return {
        _HSV_ENABLED: "true",
        _HSV_SCURVE: _HSV_SCRUVE_TEMPLATE.format(value=saturation),
    }


def _calculate_chromaticity(vibrance: int) -> Dict[str, str]:
    chromaticity = int(vibrance / 2)
    return {_LAB_ENABLED: "true", _LAB_CHROMATICITY: str(chromaticity)}
