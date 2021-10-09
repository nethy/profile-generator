from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import (
    LeftLinearEqPoint,
    LinearEqPoint,
    RightLinearEqPoint,
)
from profile_generator.schema import object_of, options_of, range_of
from profile_generator.unit import Line

_MODES = {"Aggressive": "shalbi", "Conservative": "shal"}
_IMPULSE_DENOISE_ENABLED = {"Aggressive": "true", "Conservative": "false"}


def _process(data: Any) -> Mapping[str, str]:
    mode = data.get("mode", "Conservative")
    luminance = data.get("luminance", 0)
    luminance_curve = _get_luminance_curve(luminance)
    chrominance = data.get("chrominance", 0)
    chrominance_curve = _get_chrominance_curve(chrominance)
    denoise_enabled = luminance > 0 or chrominance > 0
    details_level1 = 1 + 2 * luminance / 100
    details_level2 = 1 + luminance / 100
    details_enabled = luminance > 0
    return {
        "DenoiseEnabled": str(denoise_enabled).lower(),
        "DenoiseSMethod": _MODES[mode],
        "DenoiseLCurve": luminance_curve,
        "DenoiseCCCurve": chrominance_curve,
        "ImpulseDenoiseEnabled": _IMPULSE_DENOISE_ENABLED[mode],
        "DPEEnabled": str(details_enabled).lower(),
        "DPEMult1": str(round(details_level1, 2)),
        "DPEMult2": str(round(details_level2, 2)),
    }


def _get_luminance_curve(luminance: int) -> str:
    if luminance > 0:
        luma_eq = [LeftLinearEqPoint(0, luminance / 100), LinearEqPoint(1, 0)]
        return "1;" + raw_therapee.present_equalizer(luma_eq)
    else:
        return "0;"


def _get_chrominance_curve(chrominance: int) -> str:
    if chrominance > 0:
        chroma_line = Line(-2, chrominance / 100)
        chroma_eq = [
            LinearEqPoint(0, chroma_line.get_y(0)),
            RightLinearEqPoint(chroma_line.get_x(0), 0),
        ]
        return "1;" + raw_therapee.present_equalizer(chroma_eq)
    else:
        return "0;"


SCHEMA = object_of(
    {
        "mode": options_of("Conservative", "Aggressive"),
        "luminance": range_of(0, 100),
        "chrominance": range_of(0, 100),
    },
    _process,
)
