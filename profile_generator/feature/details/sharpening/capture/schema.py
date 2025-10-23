from profile_generator.schema import object_of
from profile_generator.schema.range_schema import range_of

SCHEMA = object_of({"radius": range_of(0.0, 2.0), "threshold": range_of(0, 200)})
