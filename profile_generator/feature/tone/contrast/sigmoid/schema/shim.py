from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_GREY18 = 90.0
_DEFAULT_EV_COMP = 0.0
_DEFAULT_GAMMA = 1.0

_CURVE = "Curve"


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[float, float, bool, float, tuple[float, float]]:
    grey18 = configuration.get("grey18", _DEFAULT_GREY18)
    gamma = configuration.get("gamma", _DEFAULT_GAMMA)
    hl_protection = configuration.get("highlight_protection", False)
    ev_comp = configuration.get("exposure_compensation", _DEFAULT_EV_COMP)
    offsets = _get_offsets(configuration)
    return (grey18, gamma, hl_protection, ev_comp, offsets)


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
    return {_CURVE: value}
