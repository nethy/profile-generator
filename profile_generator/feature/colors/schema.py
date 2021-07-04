from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

from .hsl import schema as hsl
from .white_balance import schema as white_balance

_LAB_ENABLED = "LabEnabled"
_LAB_CHROMACITY = "LabChromacity"
_LAB_SKIN_PROTECTION = "LabRASTProtection"


_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_CHROMACITY: "0",
    _LAB_SKIN_PROTECTION: "0",
    **white_balance.DEFAULT,
    **hsl.DEFAULT,
}

_DEFAULT_VIBRANCE = 0
_DEFAULT_SKIN_PROTECTION = 0


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    skin_protection = _get_skin_protection(data)
    wb_result = white_balance.process(data)
    hsl_result = hsl.process(data.get("hsl", {}))
    return _DEFAULT | vibrance | skin_protection | wb_result | hsl_result


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get("vibrance", _DEFAULT_VIBRANCE)
    is_enabled = str(vibrance != 0).lower()
    return {_LAB_ENABLED: is_enabled, _LAB_CHROMACITY: str(vibrance)}


def _get_skin_protection(data: Any) -> Mapping[str, str]:
    protection = data.get("skin_tone_protection", _DEFAULT_SKIN_PROTECTION)
    return {_LAB_SKIN_PROTECTION: str(protection)}


SCHEMA = object_of(
    {
        "vibrance": range_of(-100, 100),
        "skin_tone_protection": range_of(0, 100),
        "white_balance": white_balance.SCHEMA,
        "hsl": hsl.SCHEMA,
    },
    _process,
)
