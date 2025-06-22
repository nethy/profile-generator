from profile_generator.main.profile_params import ColorToningChannel
from profile_generator.schema.object_schema import object_of
from profile_generator.schema.options_schema import options_of
from profile_generator.schema.range_schema import range_of
from profile_generator.schema.tuple_schema import tuple_of

_LCH_VALUE_SCHEMA = tuple_of(
    range_of(-10.0, 10.0),
    range_of(0.0, 20.0),
    range_of(0.0, 360.0),
)

_TONING_SCHEMA = object_of(
    {
        "channels": options_of(*[item.name for item in ColorToningChannel]),
        "black": _LCH_VALUE_SCHEMA,
        "shadow": _LCH_VALUE_SCHEMA,
        "midtone": _LCH_VALUE_SCHEMA,
        "highlight": _LCH_VALUE_SCHEMA,
        "white": _LCH_VALUE_SCHEMA,
    }
)


_MATTE_SCHEMA = object_of(
    {
        "black": range_of(0, 20),
        "white": range_of(80, 100),
    }
)


_LCH_ADJUSTMENT_SCHEMA = object_of(
    {
        "magenta": range_of(-10, 10),
        "orange": range_of(-10, 10),
        "yellow": range_of(-10, 10),
        "green": range_of(-10, 10),
        "aqua": range_of(-10, 10),
        "teal": range_of(-10, 10),
        "blue": range_of(-10, 10),
        "purple": range_of(-10, 10),
        "skin_tone_protection": range_of(0, 100),
    }
)


_LCH_SCHEMA = object_of(
    {
        "luminance": _LCH_ADJUSTMENT_SCHEMA,
        "chroma": _LCH_ADJUSTMENT_SCHEMA,
        "hue": _LCH_ADJUSTMENT_SCHEMA,
    }
)


SCHEMA = object_of(
    {
        "toning": _TONING_SCHEMA,
        "matte": _MATTE_SCHEMA,
        "lch": _LCH_SCHEMA,
    }
)
