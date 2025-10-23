from profile_generator.schema import object_of, range_of

SCHEMA = object_of(
    {
        "linear_grey18": range_of(0.01, 0.75),
        "slope": range_of(1.0, 4.0),
    }
)
