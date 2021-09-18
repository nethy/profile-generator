from collections.abc import Mapping
from typing import Any

from profile_generator.schema import composite_process, object_of, range_of

from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance

_CT_ENABLED = "CTEnabled"
_CT_SATURATION = "CTLabRegionSaturation"
_CT_POWER = "CTLabRegionPower"

_DEFAULT = {
    _CT_ENABLED: "false",
    _CT_SATURATION: "0",
    _CT_POWER: "1",
}

_DEFAULT_VIBRANCE: int = 0


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    return _DEFAULT | vibrance


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get("vibrance", _DEFAULT_VIBRANCE)
    saturation = 0
    power = 1
    if vibrance > 0:
        saturation = 5 * vibrance
        power = 1 + vibrance / 20
    else:
        saturation = 10 * vibrance
    return {
        _CT_ENABLED: str(vibrance != 0).lower(),
        _CT_SATURATION: str(saturation),
        _CT_POWER: str(round(power, 3)),
    }


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
