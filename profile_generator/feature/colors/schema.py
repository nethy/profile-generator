from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.schema import composite_process, object_of, range_of
from profile_generator.unit import Point

from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance

_LAB_ENABLED = "LabEnabled"
_LAB_CHROMACITY = "LabChromacity"
_HSVE_ENABLED = "HSVEEnabled"
_HSVE_SCURVE = "HSVESCurve"
_CT_ENABLED = "CTEnabled"
_CT_POWER = "CTLabRegionPower"

_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_CHROMACITY: "0",
    _HSVE_ENABLED: "false",
    _HSVE_SCURVE: raw_therapee.CurveType.LINEAR,
    _CT_ENABLED: "false",
    _CT_POWER: "1",
}

_DEFAULT_VIBRANCE = 0
_DEFAULT_CHROME = 0


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    chrome = _get_chrome(data)
    return _DEFAULT | vibrance | chrome


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get("vibrance", _DEFAULT_VIBRANCE)
    if vibrance > 0:
        skin_saturation = 0.5 * (1 + vibrance / 2 / 100)
        blue_saturation = 0.5 * (1 + vibrance / 100)
        equalizer = [Point(0.05, skin_saturation), Point(0.55, blue_saturation)]
        return {
            _LAB_ENABLED: "true",
            _LAB_CHROMACITY: str(round(vibrance / 2)),
            _HSVE_ENABLED: "true",
            _HSVE_SCURVE: raw_therapee.CurveType.STANDARD
            + raw_therapee.present_linear_equalizer(equalizer),
        }
    else:
        is_enabled = str(vibrance != 0).lower()
        return {_LAB_ENABLED: is_enabled, _LAB_CHROMACITY: str(vibrance)}


def _get_chrome(data: Any) -> Mapping[str, str]:
    chrome = data.get("chrome", _DEFAULT_CHROME)
    if chrome > 0:
        power = 1 + chrome / 200
        return {_CT_ENABLED: "true", _CT_POWER: str(round(power, 3))}
    return {}


SCHEMA = object_of(
    {
        "vibrance": range_of(-100, 100),
        "chrome": range_of(0, 100),
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
