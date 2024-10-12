from typing import Final

from profile_generator.schema import object_of, range_of, tuple_of


class Field:
    GLOBAL: Final = "global"
    SHADOW: Final = "shadow"
    MIDTONE: Final = "midtone"
    HIGHLIGHT: Final = "highlight"


_HCL_SCHEMA = tuple_of(range_of(0.0, 360.0), range_of(0.0, 10.0), range_of(-10.0, 10.0))

SCHEMA = object_of(
    {
        Field.GLOBAL: _HCL_SCHEMA,
        Field.SHADOW: _HCL_SCHEMA,
        Field.MIDTONE: _HCL_SCHEMA,
        Field.HIGHLIGHT: _HCL_SCHEMA,
    }
)
