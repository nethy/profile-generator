from typing import Any, Dict


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    enabled = configuration.get("enabled", False)
    return {"PostDemosaicSharpeningEnabled": str(enabled).lower()}
