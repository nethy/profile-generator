from collections.abc import Mapping
from typing import Any, Final

from profile_generator.schema import SchemaField, composite_process, object_of, range_of

from .grading import schema as grading
from .hsl import schema as hsl
from .profile import schema as profile
from .white_balance import schema as white_balance


class Field:
    VIBRANCE: Final = SchemaField("vibrance", 0)


class Template:
    CHROMATICITY: Final = "Chromaticity"


def _process(data: Any) -> Mapping[str, str]:
    vibrance = _get_vibrance(data)
    return {} | vibrance


def _get_vibrance(data: Any) -> Mapping[str, str]:
    vibrance = data.get(*Field.VIBRANCE)
    return {Template.CHROMATICITY: str(5 * vibrance)}


SCHEMA = object_of(
    {
        Field.VIBRANCE.name: range_of(0, 10),
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
