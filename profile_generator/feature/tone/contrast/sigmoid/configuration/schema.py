from profile_generator.configuration.schema import object_of, range_of, type_of

SCHEMA = object_of(
    grey=object_of(x=range_of(16, 240), y=range_of(64, 192)),
    strength=range_of(0.0, 100.0),
    protect_hl=type_of(bool),
)
