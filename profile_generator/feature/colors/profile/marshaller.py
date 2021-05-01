from typing import Any, Dict

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.unit import Point, Strength

_LAB_ENABLED = "LabEnabled"
_LAB_A_CURVE = "LabaCurve"
_LAB_B_CURVE = "LabbCurve"

_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_A_CURVE: "0;",
    _LAB_B_CURVE: "0;",
}


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    vibrance = configuration.get("vibrance", 0)
    args = _DEFAULT
    if vibrance != 0:
        args = {**_DEFAULT, **_calculate_curves(vibrance)}
    return args


def _calculate_curves(vibrance: int) -> Dict[str, str]:
    chroma_contrast_strength = Strength(vibrance / 2 / 100)
    curve = contrast_sigmoid.calculate(Point(0.5, 0.5), chroma_contrast_strength, 17)
    raw_curve = "1;" + "".join([p.for_raw_therapee() for p in curve])
    return {_LAB_ENABLED: "true", _LAB_A_CURVE: raw_curve, _LAB_B_CURVE: raw_curve}
