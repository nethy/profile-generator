from collections.abc import Mapping
from typing import Any


def get_profile_args(configuration: Mapping[str, Any]) -> Mapping[str, str]:
    enabled = configuration.get("enabled", False)
    return {"PostDemosaicSharpeningEnabled": str(enabled).lower()}
