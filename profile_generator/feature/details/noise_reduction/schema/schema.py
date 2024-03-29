from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import (
    EqPoint,
    LinearEqPoint,
    RightLinearEqPoint,
)
from profile_generator.schema import object_of, options_of, range_of

_AGGRESSIVE = "Aggressive"
_CONSERVATIVE = "Conservative"
_MODES = {_AGGRESSIVE: "shalbi", _CONSERVATIVE: "shal"}
_IMPULSE_DENOISE_ENABLED = {_AGGRESSIVE: "true", _CONSERVATIVE: "false"}


def _process(data: Any) -> Mapping[str, str]:
    mode = data.get("mode", _CONSERVATIVE)
    luminance = data.get("luminance", 0)
    luminance_curve = _get_luminance_curve(luminance)
    chrominance = data.get("chrominance", 0)
    chrominance_curve = _get_chrominance_curve(chrominance)
    denoise_enabled = luminance > 0 or chrominance > 0
    micro_sharpening_strength = _get_micro_sharpening(mode, luminance)
    micro_sharpening_enabled = micro_sharpening_strength > 0
    return {
        "DenoiseEnabled": str(denoise_enabled).lower(),
        "DenoiseSMethod": _MODES[mode],
        "DenoiseLCurve": luminance_curve,
        "DenoiseCCCurve": chrominance_curve,
        "ImpulseDenoiseEnabled": _IMPULSE_DENOISE_ENABLED[mode],
        "SMEnabled": str(micro_sharpening_enabled).lower(),
        "SMStrength": str(micro_sharpening_strength),
    }


def _get_luminance_curve(luminance: int) -> str:
    luma_eq = None
    if luminance > 0:
        luma_eq = [LinearEqPoint(0, luminance / 100), EqPoint(1, 0)]
    return raw_therapee.present_equalizer(luma_eq)


def _get_chrominance_curve(chrominance: int) -> str:
    chroma_eq = None
    if chrominance > 0:
        chroma_eq = [
            LinearEqPoint(0, chrominance / 100),
            RightLinearEqPoint(1 / 3, 0),
        ]
    return raw_therapee.present_equalizer(chroma_eq)


def _get_micro_sharpening(mode: str, luminance: float) -> int:
    multiplier = 0.5
    if mode == _AGGRESSIVE:
        multiplier = 2.0
    return min(round(luminance * multiplier), 100)


SCHEMA = object_of(
    {
        "mode": options_of(_CONSERVATIVE, _AGGRESSIVE),
        "luminance": range_of(0, 100),
        "chrominance": range_of(0, 100),
    },
    _process,
)
