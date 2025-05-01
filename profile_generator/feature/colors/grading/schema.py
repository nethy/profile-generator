from typing import Final

from profile_generator.schema.object_schema import object_of

from .bsh import SCHEMA as BSH_SCHEMA
from .matte import SCHEMA as MATTE_SCHEMA
from .toning import SCHEMA as TONING_SCHEMA

SCHEMA = object_of(
    {
        "bsh": BSH_SCHEMA,
        "toning": TONING_SCHEMA,
        "matte": MATTE_SCHEMA,
    }
)
