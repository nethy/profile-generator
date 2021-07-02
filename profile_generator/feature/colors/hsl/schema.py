from profile_generator.schema import object_of, range_of

COLORS_SCHEMA = object_of(
    {
        "red": range_of(-6, 6),
        "yellow": range_of(-6, 6),
        "green": range_of(-6, 6),
        "cyan": range_of(-6, 6),
        "blue": range_of(-6, 6),
        "magenta": range_of(-6, 6),
    }
)

SCHEMA = object_of(
    {
        "hue": object_of({}),
    }
)
