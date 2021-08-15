from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of

_VALUES = {
    "amaze": "amaze",
    "amaze+vng4": "amazevng4",
    "dcb+vng4": "dcbvng4",
    "rcd+vng4": "rcdvng4",
    "lmmse": "lmmse",
}

_DEFAULT = _VALUES["amaze"]


def _process(data: Any) -> Mapping[str, str]:
    demosaic = data.get("demosaic", "")
    return {"BayerMethod": _VALUES.get(demosaic.casefold(), _DEFAULT)}


SCHEMA = object_of(
    {"demosaic": options_of("AMaZE", "AMaZE+VNG4", "DCB+VNG4", "RCD+VNG4", "LMMSE")},
    _process,
)
