from typing import Any, Dict

_VALUES = {"rcd+vng4": "rcdvng4", "lmmse": "lmmse"}

_DEFAULT = _VALUES["rcd+vng4"]


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, Any]:
    demosaic = configuration.get("demosaic", "")
    return {"BAYER_METHOD": _VALUES.get(demosaic.casefold(), _DEFAULT)}
