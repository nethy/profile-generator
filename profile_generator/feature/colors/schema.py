import math
from collections.abc import Mapping
from typing import Any, Final

from profile_generator.main import ProfileParams
from profile_generator.schema import composite_process, object_of, range_of

from .grading import schema as grading
from .hsl import schema as hsl
from .space import schema as space
from .white_balance import schema as white_balance


class Field:
    VIBRANCE: Final = "vibrance"


class Template:
    CHROMATICITY: Final = "Chromaticity"
    COLOR_TONING_ENABLED: Final = "CTEnabled"
    COLOR_TONING_SATURATION: Final = "CTSaturation"


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    return {} | vibrance


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get(Field.VIBRANCE, 0)
    return {Template.CHROMATICITY: str(5 * vibrance)}


SCHEMA = object_of(
    {
        Field.VIBRANCE: range_of(0, 10),
        "white_balance": white_balance.SCHEMA,
        "hsl": hsl.SCHEMA,
        "profile": space.SCHEMA,
        "grading": grading.SCHEMA,
    },
    composite_process(
        _process,
        {
            "white_balance": white_balance.process,
            "hsl": hsl.process,
            "profile": space.process,
            "grading": grading.process,
        },
    ),
)


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    vibrance = profile_params.colors.vibrance.value
    gradient = profile_params.tone.curve.sigmoid.slope.value
    strength = math.sqrt((1 - vibrance / 10) + vibrance / 10 * (2 * gradient - 1))
    chromaticity = round((strength - 1) * 100)
    saturation = round((strength - 1) * 50)
    return {
        Template.CHROMATICITY: str(chromaticity),
        Template.COLOR_TONING_ENABLED: str(saturation != 0).lower(),
        Template.COLOR_TONING_SATURATION: str(saturation),
    }
