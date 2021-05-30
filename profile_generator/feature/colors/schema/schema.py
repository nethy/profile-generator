from profile_generator.schema import object_of, range_of

SCHEMA = object_of(vibrance=range_of(-100, 100))
