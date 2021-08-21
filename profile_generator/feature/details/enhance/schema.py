from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("strength", 0)
    level0 = 1 + 0.1 * value
    level1 = 1 + 0.2 * value
    level2 = 1 + 0.1 * value
    enabled = level0 != 1
    return {
        "DPEEnabled": str(enabled).lower(),
        "DPEMult0": str(round(level0, 2)),
        "DPEMult1": str(round(level1, 2)),
        "DPEMult2": str(round(level2, 2)),
    }


SCHEMA = object_of({"strength": range_of(0, 5)}, _process)
