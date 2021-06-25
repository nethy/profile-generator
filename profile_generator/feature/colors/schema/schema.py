from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of

_LAB_ENABLED = "LabEnabled"
_LAB_CHROMACITY = "LabChromacity"
_WB_SETTING = "WB_Setting"
_WB_TEMPERATURE = "WB_Temperature"
_WB_GREEN = "WB_Green"

_DEFAULT = {
    _LAB_ENABLED: "false",
    _LAB_CHROMACITY: "0",
    _WB_SETTING: raw_therapee.WbSetting.CAMERA,
    _WB_TEMPERATURE: "6504",
    _WB_GREEN: "1",
}

_DEFAULT_VIBRANCE = 0
_DEFAULT_WB_TEMP = 6504
_DEFAULT_WB_TINT = 1


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    white_balance = _get_white_balance(data)
    return _DEFAULT | vibrance | white_balance


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get("vibrance", _DEFAULT_VIBRANCE)
    is_enabled = str(vibrance != 0).lower()
    return {_LAB_ENABLED: is_enabled, _LAB_CHROMACITY: str(vibrance)}


def _get_white_balance(data: Any) -> Mapping[str, str]:
    white_balance = data.get("white_balance", {})
    temperature = white_balance.get("temperature", _DEFAULT_WB_TEMP)
    tint = white_balance.get("tint", _DEFAULT_WB_TINT)
    result = {}
    if temperature != _DEFAULT_WB_TEMP:
        result[_WB_TEMPERATURE] = str(temperature)

    if tint != _DEFAULT_WB_TINT:
        result[_WB_GREEN] = str(tint)

    if len(result) > 0:
        result[_WB_SETTING] = raw_therapee.WbSetting.CUSTOM

    return result


_WB_SCHEMA = object_of(
    {"temperature": range_of(1500, 60000), "tint": range_of(0.02, 10.0)}
)
SCHEMA = object_of(
    {"vibrance": range_of(-100, 100), "white_balance": _WB_SCHEMA}, _process
)
