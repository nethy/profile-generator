from profile_generator.configuration.schema import object_of, range_of

SCHEMA = object_of(vibrance=range_of(-100, 100))
