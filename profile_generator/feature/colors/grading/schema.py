from profile_generator.schema.object_schema import object_of

from .matte import SCHEMA as MATTE_SCHEMA
from .toning import SCHEMA as TONING_SCHEMA

SCHEMA = object_of(
    {
        "toning": TONING_SCHEMA,
        "matte": MATTE_SCHEMA,
    }
)
