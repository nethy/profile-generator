from typing import Final

from profile_generator.schema import object_of, range_of


class Field:
    LOCAL: Final = "local"


SCHEMA = object_of({Field.LOCAL: range_of(0.0, 10.0)})
