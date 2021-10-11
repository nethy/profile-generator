import math
from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

_DEFAULT_RESOLUTION_MP = 16


def _process(data: Any) -> Mapping[str, str]:
    image_size = data.get("resolution_mp", _DEFAULT_RESOLUTION_MP)
    radius = max(1, min(100, 15 * math.sqrt(image_size)))
    value = str(round(radius))
    return {"SHRadius": value, "LCRadius": value}


SCHEMA = object_of({"resolution_mp": range_of(1.0, 1000.0)}, _process)
