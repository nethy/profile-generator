from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model import colorspace
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_GREY = [90.0, 90.0, 90.0]
_REFERENCE_NEUTRAL5 = [122.0, 122.0, 121.0]
_DEFAULT_EV_COMP = 0
_DEFAULT_GAMMA = 1.0
_DEFAULT_HLP = 1.0

_TEMPLATE_FIELD = "Curve"


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[Point, float, float, tuple[float, float]]:
    grey = _get_grey(configuration)
    gamma = _get_gamma(configuration)
    hlp = _get_highlight_protection(configuration)
    offsets = _get_offsets(configuration)
    return (grey, gamma, hlp, offsets)


def _get_grey(configuration: Mapping[str, Any]) -> Point:
    grey = configuration.get("neutral5", _DEFAULT_GREY)
    x = sum(colorspace.normalize(grey)) / 3
    ev_comp = configuration.get("exposure_compensation", _DEFAULT_EV_COMP)
    target = colorspace.normalize(_REFERENCE_NEUTRAL5)
    target = colorspace.ev_comp_srgb(target, ev_comp)
    y = sum(target) / 3
    return Point(x, y)


def _get_gamma(configuration: Mapping[str, Any]) -> float:
    return configuration.get("gamma", _DEFAULT_GAMMA)


def _get_highlight_protection(configuration: Mapping[str, Any]) -> float:
    return configuration.get("highlight_protection", _DEFAULT_HLP)


def _get_offsets(configuration: Mapping[str, Any]) -> tuple[float, float]:
    matte_effect = configuration.get("matte_effect", False)
    if matte_effect:
        return (16 / 255, 235 / 255)
    else:
        return (0, 1)


def marshal_curve(curve: Sequence[Point]) -> Mapping[str, str]:
    value = raw_therapee.CurveType.LINEAR
    if len(curve) > 0:
        value = raw_therapee.CurveType.STANDARD + raw_therapee.present_curve(curve)
    return {_TEMPLATE_FIELD: value}
