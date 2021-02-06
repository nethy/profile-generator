from typing import Any, Dict

_VALUES = {"rcd+vng4": "rcdvng4", "lmmse": "lmmse"}

_DEFAULT = _VALUES["rcd+vng4"]


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    demosaic = configuration.get("demosaic", "")
    return {"BayerMethod": _VALUES.get(demosaic.casefold(), _DEFAULT)}
