from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.schema import composite_process, object_of, range_of
from profile_generator.unit import Point

from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance

_HSV_ENABLED = "HSVEnabled"
_HSV_SCURVE = "HSVSCurve"
_CHROMATICITY = "Chromaticity"

_DEFAULT = {_HSV_ENABLED: "false", _HSV_SCURVE: "0;", _CHROMATICITY: "0"}

_DEFAULT_VIBRANCE = 0


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    return _DEFAULT | vibrance


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get("vibrance", _DEFAULT_VIBRANCE)
    if vibrance > 0:
        strength = 0.05 * vibrance
        return {
            _HSV_ENABLED: "true",
            _HSV_SCURVE: raw_therapee.CurveType.STANDARD
            + raw_therapee.present_equalizer(
                (Point(15 / 360, strength / 2 + 0.5), Point(195 / 360, strength + 0.5))
            ),
        }
    else:
        return {_CHROMATICITY: str(round(vibrance * 10))}


SCHEMA = object_of(
    {
        "vibrance": range_of(-10, 10),
        "white_balance": white_balance.SCHEMA,
        "hsl": hsl.SCHEMA,
        "profile": profile.SCHEMA,
    },
    composite_process(
        _process,
        {
            "white_balance": white_balance.process,
            "hsl": hsl.process,
            "profile": profile.process,
        },
    ),
)
