from profile_generator.schema import object_of, range_of

from .grading import schema as grading

SCHEMA = object_of(
    {
        "vibrance": range_of(0.0, 10.0),
        "grading": grading.SCHEMA,
    }
)
