from profile_generator.schema import object_of, range_of

SCHEMA = object_of(
    {
        "strength": range_of(0, 100),
    }
)
