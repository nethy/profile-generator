from collections.abc import Mapping
from typing import Any, Final

from profile_generator.schema import object_of, range_of
from profile_generator.schema.schema import SchemaField

from .grading import schema as grading
from .hsl import schema as hsl
from .space import schema as space
from .white_balance import schema as white_balance


class Field:
    VIBRANCE: Final = SchemaField("vibrance", 0)


class Template:
    VIBRANCE_ENABLED: Final = "VibranceEnabled"
    VIBRANCE_PASTELS: Final = "VibrancePastels"
    VIBRANCE_SATURATED: Final = "VibranceSaturated"


_MAX_VIBRANCE: Final = 10


def _process(data: Any) -> Mapping[str, str]:
    vibrance = data.get(*Field.VIBRANCE)
    pastels = round(100 * vibrance / _MAX_VIBRANCE)
    saturated = round(pastels / 2)
    return {
        Template.VIBRANCE_ENABLED: str(vibrance > Field.VIBRANCE.default_value).lower(),
        Template.VIBRANCE_PASTELS: str(pastels),
        Template.VIBRANCE_SATURATED: str(saturated),
    }


SCHEMA = object_of(
    {
        Field.VIBRANCE.name: range_of(0, _MAX_VIBRANCE),
        "white_balance": white_balance.SCHEMA,
        "hsl": hsl.SCHEMA,
        "profile": space.SCHEMA,
        "grading": grading.SCHEMA,
    }
)
