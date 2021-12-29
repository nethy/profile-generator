from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import LinearEqPoint
from profile_generator.schema import object_of, range_of

_WL_ENABLED = "WaveletEnabled"
_WL_CURVE = "WaveletOpacityCurveWL"

_DEFAULT_LOCAL_CONTRAST = 0


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("local", _DEFAULT_LOCAL_CONTRAST)
    amount = 0.5 + 0.05 * value
    curve = raw_therapee.CurveType.STANDARD + raw_therapee.present_equalizer(
        (
            LinearEqPoint(0.15, 0.5),
            LinearEqPoint(0.35, amount),
            LinearEqPoint(0.65, amount),
            LinearEqPoint(0.85, 0.5),
        )
    )
    enabled = str(value > _DEFAULT_LOCAL_CONTRAST).lower()
    return {_WL_ENABLED: enabled, _WL_CURVE: curve}


SCHEMA = object_of({"local": range_of(0, 10)}, _process)
