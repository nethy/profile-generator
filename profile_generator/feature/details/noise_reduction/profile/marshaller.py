from typing import Any, Dict


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, Any]:
    enabled = configuration.get("enabled", False)
    strength = configuration.get("strength", 10)
    median = configuration.get("median", False)
    return {
        "DenoisingEnabled": str(enabled).lower(),
        "DenoisingLCurve": f"1;0.2;{strength/100:.2f};0;0;1;0;0;0;",
        "Median": str(median).lower(),
    }
