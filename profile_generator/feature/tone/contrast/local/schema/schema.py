from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of
from profile_generator.unit import Point

_ENABLED_FIELD = "WaveletEnabled"
_CURVE_FIELD = "OpacityCurveWL"

_LINEAR_CURVE = "0;"


def _process(data: Any) -> Mapping[str, str]:
    local = data.get("local", 0)
    is_enabled = False
    raw_eq_curve = _LINEAR_CURVE
    if local > 0:
        is_enabled = True
        y = 0.5 * (1 + local / 100)
        eq_curve = [Point(0, 0.5), Point(0.4, y), Point(0.6, y), Point(1, 0.5)]
        raw_eq_curve = "1;" + raw_therapee.present_equalizer(eq_curve)
    return {_ENABLED_FIELD: str(is_enabled).lower(), _CURVE_FIELD: raw_eq_curve}


SCHEMA = object_of({"local": range_of(0, 100)}, _process)
