from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of

_OFF = "off"
_AA = "aa"
_NO_AA = "no_aa"

_RADIUS = {_OFF: 0.5, _AA: 0.7, _NO_AA: 0.59}


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("type", _OFF)
    return {
        "PDSEnabled": str(value != _OFF).lower(),
        "PDSDeconvRadius": str(_RADIUS[value]),
    }


SCHEMA = object_of({"type": options_of(_OFF, _AA, _NO_AA)}, _process)
