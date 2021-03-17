from typing import Any, Dict

_VALUES = {"dcb+vng4": "dcbvng4", "lmmse": "lmmse"}

_DEFAULT = _VALUES["dcb+vng4"]


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    demosaic = configuration.get("demosaic", "")
    return {"BayerMethod": _VALUES.get(demosaic.casefold(), _DEFAULT)}
