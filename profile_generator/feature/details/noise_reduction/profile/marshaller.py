from typing import Any, Dict

from profile_generator.functions import equalizer
from profile_generator.unit import Point


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    enabled = configuration.get("enabled", False)
    strength = configuration.get("strength", 10)
    median = configuration.get("median", False)
    luminance_curve = equalizer.to_raw_therapee(Point(0.2, strength / 100), Point(1, 0))
    chroma_curve = equalizer.to_raw_therapee(Point(0, 0.5), Point(0.25, 0))
    return {
        "DenoiseEnabled": str(enabled).lower(),
        "DenoiseLCurve": luminance_curve,
        "DenoiseCCCurve": chroma_curve,
        "Median": str(median).lower(),
    }
