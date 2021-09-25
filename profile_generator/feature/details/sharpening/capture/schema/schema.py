from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of
from profile_generator.schema.range_schema import range_of


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("radius", 0.0)
    if value < 0.399999999:
        value = 0.0
    return {
        "PDSEnabled": str(value > 0.0).lower(),
        "PDSDeconvRadius": str(round(value, 2)),
    }


SCHEMA = object_of({"radius": range_of(0.0, 2.0)}, _process)
