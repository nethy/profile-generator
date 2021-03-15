from profile_generator.configuration.schema import object_of, range_of, type_of

SCHEMA = object_of(
    enabled=type_of(bool),
    threshold=range_of(0, 200),
    radius=range_of(0.4, 2.5),
    amount=range_of(0, 100),
    damping=range_of(0, 100),
    iterations=range_of(5, 100),
)
