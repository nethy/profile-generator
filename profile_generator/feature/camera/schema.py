import math
from collections.abc import Mapping
from typing import Any, Final

from profile_generator.profile_params import ProfileParams
from profile_generator.schema import object_of, range_of

_DEFAULT_RESOLUTION_MP = 16


class Field:
    RESOLUTION: Final = "resolution_mp"


class Template:
    SHADOW_HIGHLIGHT_RADIUS: Final = "SHRadius"
    LOCAL_CONTRAST_RADIUS: Final = "LCRadius"


def _process(data: Any) -> Mapping[str, str]:
    image_size = data.get(Field.RESOLUTION, _DEFAULT_RESOLUTION_MP)
    radius = max(1, min(100, 15 * math.sqrt(image_size)))
    value = str(round(radius))
    return {
        Template.SHADOW_HIGHLIGHT_RADIUS: value,
        Template.LOCAL_CONTRAST_RADIUS: value,
    }


def _parse(data: Any, profile_input: ProfileParams) -> None:
    profile_input.camera.resolution_mp = data.get(Field.RESOLUTION)


SCHEMA = object_of({Field.RESOLUTION: range_of(1.0, 1000.0)}, _process, _parse)
