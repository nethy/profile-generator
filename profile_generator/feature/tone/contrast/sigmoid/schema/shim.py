from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.linalg import Vector
from profile_generator.model.sigmoid import HighlighTone
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_NETRUAL5: Vector = [90, 90, 90]
_DEFAULT_EV_COMP = 0.0
_DEFAULT_GAMMA = 1.0

_TEMPLATE_FIELD = "Curve"

_HL_TONES = {
    "NORMAL": HighlighTone.NORMAL,
    "INCREASED": HighlighTone.INCREASED,
    "DECREASED": HighlighTone.DECREASED,
}


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[Vector, float, HighlighTone, float, tuple[float, float]]:
    netrual5 = configuration.get("neutral5", _DEFAULT_NETRUAL5)
    ev_comp = configuration.get("exposure_compensation", _DEFAULT_EV_COMP)
    hl_tone = _get_hl_tone(configuration)
    gamma = configuration.get("gamma", _DEFAULT_GAMMA)
    offsets = _get_offsets(configuration)
    return (netrual5, gamma, hl_tone, ev_comp, offsets)


def _get_hl_tone(configuration: Mapping[str, Any]) -> HighlighTone:
    hl_tone = configuration.get("highlight_tone", "NORMAL")
    return _HL_TONES.get(hl_tone, HighlighTone.NORMAL)


def _get_offsets(configuration: Mapping[str, Any]) -> tuple[float, float]:
    matte_effect = configuration.get("matte_effect", False)
    if matte_effect:
        return (16 / 255, 1.0)
    else:
        return (0, 1)


def marshal_curve(curve: Sequence[Point]) -> Mapping[str, str]:
    value = raw_therapee.CurveType.LINEAR
    if len(curve) > 0:
        value = raw_therapee.CurveType.STANDARD + raw_therapee.present_curve(curve)
    return {_TEMPLATE_FIELD: value}
