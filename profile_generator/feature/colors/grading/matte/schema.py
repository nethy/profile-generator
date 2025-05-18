from profile_generator.schema.object_schema import object_of
from profile_generator.schema.range_schema import range_of

SCHEMA = object_of(
    {
        "shadow": range_of(0, 55),
        "highlight": range_of(200, 255),
    }
)
