from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model import linalg
from profile_generator.model.colorspace import lab, rgb, xyz
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
    color = [rgb.srgb_gamma_inverse(x) for x in rgb.normalize(color)]
    return rgb.srgb_luminance(color)


def _set_middle_grey(in_lum: float, out_lum: float, ev_comp: float) -> Point:
    linear_middle_grey = lab.lab_to_xyz([50, 0, 0], xyz.D50_XYZ)
    linear_middle_grey = linalg.transform(xyz.XYZ_TO_SRGB, linear_middle_grey)
    middle_grey_lum = rgb.srgb_luminance(linear_middle_grey)
    x = in_lum * middle_grey_lum / out_lum
    return Point(rgb.srgb_gamma(x), rgb.srgb_gamma(middle_grey_lum * 2 ** ev_comp))


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
