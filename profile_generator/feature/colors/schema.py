from collections.abc import Mapping
from typing import Any, Final

from profile_generator.schema import SchemaField, composite_process, object_of, range_of

from .grading import schema as grading
from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance


class Field:
    VIBRANCE: Final = SchemaField("vibrance", 0)
    CHROME: Final = SchemaField("chrome", 0)


class Template:
    CHROMATICITY: Final = "Chromaticity"
    COLOR_TONING_ENABLED: Final = "CTEnabled"
    COLOR_TONING_POWER: Final = "CTLabRegionPower"
    COLOR_TONING_SLOPE: Final = "CTLabRegionSlope"


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    chrome = _get_chrome(data)
    return {} | vibrance | chrome


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get(*Field.VIBRANCE)
    chromaticity = 5 * vibrance
    return {Template.CHROMATICITY: str(chromaticity)}


def _get_chrome(data: Any) -> Mapping[str, str]:
    chrome = data.get(*Field.CHROME)
    enabled = chrome > 0
    slope = 1 - 0.05 * chrome
    return {
        Template.COLOR_TONING_ENABLED: str(enabled).lower(),
        Template.COLOR_TONING_SLOPE: str(round(slope, 3)),
    }


SCHEMA = object_of(
    {
        Field.VIBRANCE.name: range_of(0, 10),
        Field.CHROME.name: range_of(0, 10),
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
