from profile_generator.schema import object_of, range_of

LAB_SCHEMA = object_of(
    {
        "l": range_of(0.0, 100.0),
        "a": range_of(-127.0, 127.0),
        "b": range_of(-127.0, 127.0),
    }
)

SCHEMA = object_of(
    {
        "blue": LAB_SCHEMA,
        "green": LAB_SCHEMA,
        "red": LAB_SCHEMA,
        "yellow": LAB_SCHEMA,
        "magenta": LAB_SCHEMA,
        "cyan": LAB_SCHEMA,
        "white": LAB_SCHEMA,
        "neutral8": LAB_SCHEMA,
        "neutral6.5": LAB_SCHEMA,
        "neutral5": LAB_SCHEMA,
        "neutral3.5": LAB_SCHEMA,
        "black": LAB_SCHEMA,
    }
)
