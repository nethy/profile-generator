from profile_generator.schema.list_schema import list_of
from profile_generator.schema.range_schema import range_of
from profile_generator.schema.tuple_schema import tuple_of

_TONE_SCHEMA = tuple_of(
    range_of(0.0, 100.0),
    range_of(0.0, 100.0),
    range_of(0.0, 100.0),
    range_of(0.0, 360.0),
)

SCHEMA = list_of(_TONE_SCHEMA)
