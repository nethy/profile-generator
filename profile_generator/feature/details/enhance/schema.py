from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of


def _process(data: Any) -> Mapping[str, str]:
    strength = data.get("strength", 0)
    level = 1 + 0.2 * strength
    value = round(level, 2)
    enabled = level >= 1.01
    return {
        "DPEEnabled": str(enabled).lower(),
        "DPEMult0": str(value),
        "DPEMult1": str(value),
    }


SCHEMA = object_of({"strength": range_of(0.0, 5.0)}, _process)
