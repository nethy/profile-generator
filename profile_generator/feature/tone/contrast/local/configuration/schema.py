from profile_generator.configuration.schema import object_of, range_of

SCHEMA = object_of(local=range_of(0, 100))
