from typing import Final, Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee


class Template:
    WB_SETTING: Final = "WBSetting"
    WB_TEMPERATURE: Final = "WBTemperature"
    WB_GREEN: Final = "WBGreen"


DEFAULT = {
    Template.WB_SETTING: raw_therapee.WbSetting.CAMERA,
    Template.WB_TEMPERATURE: "6504",
    Template.WB_GREEN: "1",
}

_DEFAULT_WB_TEMP = 6504
_DEFAULT_WB_TINT = 1


class Field:
    TEMPERATURE: Final = "temperature"
    TINT: Final = "tint"


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    temperature = profile_params.colors.white_balance.temperature.value
    tint = profile_params.colors.white_balance.tint.value
    result = {}
    if temperature != _DEFAULT_WB_TEMP:
        result[Template.WB_TEMPERATURE] = str(temperature)

    if tint != _DEFAULT_WB_TINT:
        result[Template.WB_GREEN] = str(tint)

    if len(result) > 0:
        result[Template.WB_SETTING] = raw_therapee.WbSetting.CUSTOM

    return DEFAULT | result
