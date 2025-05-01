from collections.abc import Mapping, Sequence
from typing import Any, Final

from profile_generator.feature.colors.white_balance.schema import DEFAULT
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint, LinearEqPoint
from profile_generator.schema import object_of, range_of
from profile_generator.schema.tuple_schema import tuple_of

_STEPS = 10.0

_BSH_SCHEMA = tuple_of(
    range_of(-_STEPS, _STEPS),
    range_of(-_STEPS, _STEPS),
    range_of(-_STEPS, _STEPS),
)

SCHEMA = object_of(
    {
        "red": _BSH_SCHEMA,
        "yellow": _BSH_SCHEMA,
        "green": _BSH_SCHEMA,
        "cyan": _BSH_SCHEMA,
        "blue": _BSH_SCHEMA,
        "magenta": _BSH_SCHEMA,
    }
)

