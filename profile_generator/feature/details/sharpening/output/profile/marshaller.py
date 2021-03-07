from typing import Any, Dict


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    enabled = configuration.get("enabled", False)
    threshold = configuration.get("threshold", 20)
    radius = configuration.get("radius", 0.75)
    amount = configuration.get("amount", 100)
    iterations = configuration.get("iterations", 30)
    return {
        "SharpeningEnabled": str(enabled).lower(),
        "SharpeningContrast": str(threshold),
        "DeconvRadius": f"{radius:.2f}",
        "DeconvAmount": str(amount),
        "DeconvIterations": str(iterations),
    }
