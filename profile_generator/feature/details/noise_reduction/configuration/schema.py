from profile_generator.configuration.schema import object_of, range_of, type_of

SCHEMA = object_of(
    enabled=type_of(bool), strength=range_of(0, 100), median=type_of(bool)
)
