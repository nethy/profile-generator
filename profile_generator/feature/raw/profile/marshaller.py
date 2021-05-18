from collections.abc import Mapping
from typing import Any

_VALUES = {"dcb+vng4": "dcbvng4", "lmmse": "lmmse"}

_DEFAULT = _VALUES["dcb+vng4"]


def get_profile_args(configuration: Mapping[str, Any]) -> Mapping[str, str]:
    demosaic = configuration.get("demosaic", "")
    return {"BayerMethod": _VALUES.get(demosaic.casefold(), _DEFAULT)}
