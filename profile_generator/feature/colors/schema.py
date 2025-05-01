from profile_generator.schema import object_of, range_of

from .grading import schema as grading
from .space import schema as space
from .white_balance import schema as white_balance

SCHEMA = object_of(
    {
        "vibrance": range_of(0, 10),
        "white_balance": white_balance.SCHEMA,
        "profile": space.SCHEMA,
        "grading": grading.SCHEMA,
    }
)
