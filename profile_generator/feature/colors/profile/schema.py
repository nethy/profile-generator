from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of

_VALUES = {
    "acesp0": "ACESp0",
    "acesp1": "ACESp1",
    "prophoto": "ProPhoto",
    "rec2020": "Rec2020",
    "srgb": "sRGB",
}
_DEFAULT_VALUE = "prophoto"


def process(data: Any) -> Mapping[str, str]:
    value = data.get("working", _DEFAULT_VALUE)
    value = value.casefold()
    return {"CMWorkingProfile": _VALUES[value]}


SCHEMA = object_of({"working": options_of(*_VALUES.keys())})
