from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of

_WB_SETTING = "WBSetting"
_WB_TEMPERATURE = "WBTemperature"
_WB_GREEN = "WBGreen"

DEFAULT = {
    _WB_SETTING: raw_therapee.WbSetting.CAMERA,
    _WB_TEMPERATURE: "6504",
    _WB_GREEN: "1",
}

_DEFAULT_WB_TEMP = 6504
_DEFAULT_WB_TINT = 1


class Field:
    TEMPERATURE: Final = "temperature"
    TINT: Final = "tint"


SCHEMA = object_of({"temperature": range_of(1500, 60000), "tint": range_of(0.02, 10.0)})


def process(data: Any) -> Mapping[str, str]:
    temperature = data.get("temperature", _DEFAULT_WB_TEMP)
    tint = data.get("tint", _DEFAULT_WB_TINT)
    result = {}
    if temperature != _DEFAULT_WB_TEMP:
        result[_WB_TEMPERATURE] = str(temperature)

    if tint != _DEFAULT_WB_TINT:
        result[_WB_GREEN] = str(tint)

    if len(result) > 0:
        result[_WB_SETTING] = raw_therapee.WbSetting.CUSTOM

    return DEFAULT | result
