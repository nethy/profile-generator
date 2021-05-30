from profile_generator.schema import object_of, options_of, range_of

SCHEMA = object_of(
    mode=options_of("Conservative", "Aggressive"),
    luminance=range_of(0, 100),
    chrominance=range_of(0, 100),
)
