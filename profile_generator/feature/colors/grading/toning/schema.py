from profile_generator.main.profile_params import ColorToningChannel
from profile_generator.schema.object_schema import object_of
from profile_generator.schema.options_schema import options_of
from profile_generator.schema.range_schema import range_of
from profile_generator.schema.tuple_schema import tuple_of

_LCH_SCHEMA = tuple_of(
    range_of(-10.0, 10.0),
    range_of(0.0, 20.0),
    range_of(0.0, 360.0),
)

SCHEMA = object_of(
    {
        "channels": options_of(*[item.name for item in ColorToningChannel]),
        "black": _LCH_SCHEMA,
        "shadow": _LCH_SCHEMA,
        "midtone": _LCH_SCHEMA,
        "highlight": _LCH_SCHEMA,
        "white": _LCH_SCHEMA,
    }
)
