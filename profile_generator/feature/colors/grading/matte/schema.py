from profile_generator.schema.object_schema import object_of
from profile_generator.schema.range_schema import range_of

SCHEMA = object_of(
    {
        "black": range_of(0, 20),
        "white": range_of(80, 100),
    }
)
