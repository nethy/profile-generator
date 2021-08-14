import math
from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

_DEFAULT_IMAGE_SIZE_IN_MP = 16


def _process(data: Any) -> Mapping[str, str]:
    image_size = data.get("image_size_in_mp", _DEFAULT_IMAGE_SIZE_IN_MP)
    radius = max(1, min(100, 10 * math.sqrt(image_size)))
    return {"SHRadius": str(round(radius))}


SCHEMA = object_of({"image_size_in_mp": range_of(1.0, 1000.0)}, _process)
