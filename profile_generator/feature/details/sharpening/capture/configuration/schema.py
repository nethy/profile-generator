from profile_generator.configuration.schema import object_of, type_of

SCHEMA = object_of(enabled=type_of(bool))
