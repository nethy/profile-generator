from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of

_WB_SETTING = "WB_Setting"
_WB_TEMPERATURE = "WB_Temperature"
_WB_GREEN = "WB_Green"

DEFAULT = {
    _WB_SETTING: raw_therapee.WbSetting.CAMERA,
    _WB_TEMPERATURE: "6504",
    _WB_GREEN: "1",
}

_DEFAULT_WB_TEMP = 6504
_DEFAULT_WB_TINT = 1

SCHEMA = object_of({"temperature": range_of(1500, 60000), "tint": range_of(0.02, 10.0)})


def process(data: Any) -> Mapping[str, str]:
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
