from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of
from profile_generator.schema.range_schema import range_of


def _process(data: Any) -> Mapping[str, str]:
    radius = data.get("radius", 0.0)
    if radius < 0.399999999:
        radius = 0.0
    threshold = data.get("threshold", 10)
    return {
        "PDSEnabled": str(radius > 0.0).lower(),
        "PDSDeconvRadius": str(round(radius, 2)),
        "PDSContrast": str(threshold),
    }


SCHEMA = object_of(
    {"radius": range_of(0.0, 2.0), "threshold": range_of(0, 200)}, _process
)
