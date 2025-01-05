from typing import Final

from profile_generator.schema import object_of, range_of, tuple_of

from . import demosaic

_RANGE: Final = range_of(-2048, 2048)


SCHEMA = object_of(
    {
        "demosaic": demosaic.SCHEMA,
        "black_points": tuple_of(_RANGE, _RANGE, _RANGE),
    }
)
