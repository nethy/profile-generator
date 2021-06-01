from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of

_VALUES = {"dcb+vng4": "dcbvng4", "lmmse": "lmmse"}

_DEFAULT = _VALUES["dcb+vng4"]


def _process(data: Any) -> Mapping[str, str]:
    demosaic = data.get("demosaic", "")
    return {"BayerMethod": _VALUES.get(demosaic.casefold(), _DEFAULT)}


SCHEMA = object_of({"demosaic": options_of("RCD+VNG4", "LMMSE")}, _process)
