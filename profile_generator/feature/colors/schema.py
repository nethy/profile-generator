import math
from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import LinearEqPoint
from profile_generator.schema import composite_process, object_of, range_of

from .grading import schema as grading
from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance


class Field:
    VIBRANCE: Final = "vibrance"
    CHROME: Final = "chrome"


class Template:
    HSV_ENABLED: Final = "HSVEnabled"
    HSV_SCURVE: Final = "HSVSCurve"
    COLOR_TONING_ENABLED: Final = "CTEnabled"
    COLOR_TONING_POWER: Final = "CTLabRegionPower"
    COLOR_TONING_SLOPE: Final = "CTLabRegionSlope"


_DEFAULT = {
    Template.HSV_ENABLED: "false",
    Template.HSV_SCURVE: "0;",
    Template.COLOR_TONING_ENABLED: "false",
    Template.COLOR_TONING_POWER: "1",
    Template.COLOR_TONING_SLOPE: "1",
}


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    chrome = _get_chrome(data)
    return _DEFAULT | vibrance | chrome


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get(Field.VIBRANCE, 0)
    if math.isclose(vibrance, 0):
        return {Template.HSV_ENABLED: "false", Template.HSV_SCURVE: "0;"}

    strength = 0.05 * vibrance
    return {
        Template.HSV_ENABLED: "true",
        Template.HSV_SCURVE: raw_therapee.CurveType.STANDARD
        + raw_therapee.present_equalizer(
            (
                LinearEqPoint(30 / 360, strength / 2 + 0.5),
                LinearEqPoint(90 / 360, strength + 0.5),
                LinearEqPoint(270 / 360, strength + 0.5),
                LinearEqPoint(330 / 360, strength / 2 + 0.5),
            )
        ),
    }


def _get_chrome(data: Any) -> Mapping[str, str]:
    chrome = data.get(Field.CHROME, 0)
    if chrome < 0.01:
        return {}

    slope = 1 - 0.05 * chrome
    power = 1 / slope
    return {
        Template.COLOR_TONING_ENABLED: "true",
        Template.COLOR_TONING_SLOPE: str(round(slope, 3)),
        Template.COLOR_TONING_POWER: str(round(power, 3)),
    }


SCHEMA = object_of(
    {
        Field.VIBRANCE: range_of(0, 10),
        Field.CHROME: range_of(0, 10),
        "white_balance": white_balance.SCHEMA,
        "hsl": hsl.SCHEMA,
        "profile": profile.SCHEMA,
        "grading": grading.SCHEMA,
    },
    composite_process(
        _process,
        {
            "white_balance": white_balance.process,
            "hsl": hsl.process,
            "profile": profile.process,
            "grading": grading.process,
        },
    ),
)
