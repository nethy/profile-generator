
from profile_generator.schema.object_schema import object_of
from profile_generator.schema.range_schema import range_of
from profile_generator.schema.tuple_schema import tuple_of

_LCH_SCHEMA = tuple_of(
    range_of(0.0, 100.0),
    range_of(0.0, 100.0),
    range_of(0.0, 360.0),
)

SCHEMA = object_of({
    "global_lch": _LCH_SCHEMA,
    "shadow_lch": _LCH_SCHEMA,
    "midtone_lch": _LCH_SCHEMA,
    "highlight_lch": _LCH_SCHEMA,
})
