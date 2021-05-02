from typing import Any, Dict

from profile_generator.model import equalizer
from profile_generator.unit import Point


def get_profile_args(configuration: Dict[str, Any]) -> Dict[str, str]:
    enabled = configuration.get("enabled", False)
    strength = configuration.get("strength", 10)
    median = configuration.get("median", False)
    luminance_curve = equalizer.equalize(Point(0.2, strength / 100), Point(1, 0))
    raw_luminance_curve = "1;" + "".join(
        (p.for_raw_therapee() for p in luminance_curve)
    )
    chroma_curve = equalizer.equalize(Point(0, 0.5), Point(0.25, 0))
    raw_chroma_curve = "1;" + "".join((p.for_raw_therapee() for p in chroma_curve))
    return {
        "DenoiseEnabled": str(enabled).lower(),
        "DenoiseLCurve": raw_luminance_curve,
        "DenoiseCCCurve": raw_chroma_curve,
        "Median": str(median).lower(),
    }
