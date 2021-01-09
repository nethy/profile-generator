from typing import Any, Dict


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, Any]:
    enabled = configuration.get("enabled", False)
    return {"CaptureSharpeningEnabled": str(enabled).lower()}
