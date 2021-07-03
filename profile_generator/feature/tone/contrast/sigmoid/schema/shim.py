from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.linalg import Vector
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
    in_lum = _srgb_to_luminance(grey)
    ev_comp = configuration.get("exposure_compensation", _DEFAULT_EV_COMP)
    out_lum = _srgb_to_luminance(_REFERENCE_NEUTRAL5)
    return _set_middle_grey(in_lum, out_lum, ev_comp)


def _srgb_to_luminance(color: Vector) -> float:
    color = [SRGB.inverse_gamma(x) for x in rgb.normalize(color)]
    return rgb.luminance(color, SRGB)


def _set_middle_grey(in_lum: float, out_lum: float, ev_comp: float) -> Point:
    x = in_lum * constants.SRGB_MIDDLE_GREY_LUMINANCE / out_lum
    y = constants.SRGB_MIDDLE_GREY_LUMINANCE * 2 ** ev_comp
    return Point(SRGB.gamma(x), SRGB.gamma(y))


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
