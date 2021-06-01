from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of, type_of


def _process(data: Any) -> Mapping[str, str]:
    enabled = data.get("enabled", False)
    threshold = data.get("threshold", 20)
    radius = data.get("radius", 0.75)
    amount = data.get("amount", 100)
    damping = data.get("damping", 0)
    iterations = data.get("iterations", 30)
    return {
        "SharpeningEnabled": str(enabled).lower(),
        "SharpeningContrast": str(threshold),
        "DeconvRadius": f"{radius:.2f}",
        "DeconvAmount": str(amount),
        "DeconvDamping": str(damping),
        "DeconvIterations": str(iterations),
    }


SCHEMA = object_of(
    {
        "enabled": type_of(bool),
        "threshold": range_of(0, 200),
        "radius": range_of(0.4, 2.5),
        "amount": range_of(0, 100),
        "damping": range_of(0, 100),
        "iterations": range_of(5, 100),
    },
    _process,
)
