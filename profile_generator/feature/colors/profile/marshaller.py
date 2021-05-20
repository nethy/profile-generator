from collections.abc import Mapping
from typing import Any

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.model import sigmoid
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength

_LAB_ENABLED = "LabEnabled"
_LAB_A_CURVE = "LabaCurve"
_LAB_B_CURVE = "LabbCurve"

_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_A_CURVE: raw_therapee.CurveType.LINEAR,
    _LAB_B_CURVE: raw_therapee.CurveType.LINEAR,
}


def get_profile_args(configuration: Mapping[str, Any]) -> Mapping[str, str]:
    vibrance = configuration.get("vibrance", 0)
    if vibrance == 0:
        return _DEFAULT
    else:
        return _calculate_curves(vibrance)


def _calculate_curves(vibrance: int) -> Mapping[str, str]:
    chroma_contrast = Strength(vibrance / 2 / 100)
    if chroma_contrast.value > 0:
        curve = contrast_sigmoid.calculate(Point(0.5, 0.5), chroma_contrast)
    else:
        slope = sigmoid.contrast_gradient(
            chroma_contrast.value * contrast_sigmoid.MAX_CONTRAST
        )
        curve = [Point(0, 0.5 - 0.5 / slope), Point(1, 0.5 + 0.5 / slope)]
    raw_curve = raw_therapee.CurveType.FLEXIBLE + raw_therapee.present_curve(curve)
    return {_LAB_ENABLED: "true", _LAB_A_CURVE: raw_curve, _LAB_B_CURVE: raw_curve}
