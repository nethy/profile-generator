from profile_generator.schema import object_of, range_of, tuple_of

SCHEMA = object_of(
    {
        "grey": object_of({"x": range_of(0, 255), "y": range_of(0, 255)}),
        "strength": range_of(0.0, 100.0),
        "weights": tuple_of(range_of(0.0, 5.0), range_of(0.0, 5.0)),
    }
)
