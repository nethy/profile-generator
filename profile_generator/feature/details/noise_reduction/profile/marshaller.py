from typing import Any

from profile_generator.model import equalizer
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Line, Point

_MODES = {"Aggressive": "shalbi", "Conservative": "shal"}
_IMPULSE_DENOISE_ENABLED = {"Aggressive": "true", "Conservative": "false"}


def get_profile_args(configuration: dict[str, Any]) -> dict[str, str]:
    mode = configuration.get("mode", "Conservative")
    luminance = configuration.get("luminance", 0)
    luminance_curve = _get_luminance_curve(luminance)
    chrominance = configuration.get("chrominance", 0)
    chrominance_curve = _get_chrominance_curve(chrominance)
    denoise_enabled = luminance > 0 or chrominance > 0
    return {
        "DenoiseEnabled": str(denoise_enabled).lower(),
        "DenoiseSMethod": _MODES[mode],
        "DenoiseLCurve": luminance_curve,
        "DenoiseCCCurve": chrominance_curve,
        "ImpulseDenoiseEnabled": _IMPULSE_DENOISE_ENABLED[mode],
    }


def _get_luminance_curve(luminance: int) -> str:
    if luminance > 0:
        luminance_eq = equalizer.equalize(
            Point(0, luminance / 100), Point(0.75, luminance / 100 / 4)
        )
        luminance_eq[1].left += luminance_eq[0].right
        luminance_eq[0].right = luminance_eq[0].left = 0
        luminance_eq[1].right = 0
        return "1;" + raw_therapee.present_equalizer(luminance_eq)
    else:
        return "0;"


def _get_chrominance_curve(chrominance: int) -> str:
    if chrominance > 0:
        chrome_line = Line(-2, chrominance / 100)
        chroma_eq = equalizer.equalize(
            Point(0, chrome_line.get_y(0)), Point(chrome_line.get_x(0), 0)
        )
        chroma_eq[0].left = chroma_eq[1].right = 0
        return "1;" + raw_therapee.present_equalizer(chroma_eq)
    else:
        return "0;"
