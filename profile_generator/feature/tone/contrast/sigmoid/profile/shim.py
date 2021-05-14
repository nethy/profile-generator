from collections.abc import Iterable, Mapping
from typing import Any

from profile_generator.unit import DECIMALS, Point, Strength

_DEFAULT_GREY_X = 92
_DEFAULT_GREY_Y = 119
_DEFAULT_STRENGTH = 0

_TEMPLATE_FIELD = "Curve"

_LINEAR_CURVE_ID = 0
_SPLINE_CURVE_ID = 1
_FLEXIBLE_CURVE_ID = 4


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[Point, Strength, bool, tuple[float, float]]:
    grey = _get_grey(configuration)
    strength = _get_strength(configuration)
    protect_hl = _get_protect_hl(configuration)
    offsets = _get_offsets(configuration)
    return (grey, strength, protect_hl, offsets)


def _get_grey(configuration: Mapping[str, Any]) -> Point:
    grey = configuration.get("grey", {})
    x = grey.get("x", _DEFAULT_GREY_X) / 255
    y = grey.get("y", _DEFAULT_GREY_Y) / 255
    return Point(x, y)


def _get_strength(configuration: Mapping[str, Any]) -> Strength:
    value = configuration.get("strength", _DEFAULT_STRENGTH) / 100
    return Strength(value)


def _get_protect_hl(configuration: Mapping[str, Any]) -> bool:
    return configuration.get("protect_hl", False)


def _get_offsets(configuration: Mapping[str, Any]) -> tuple[float, float]:
    matte_effect = configuration.get("matte_effect", False)
    if matte_effect:
        return (16 / 255, 235 / 255)
    else:
        return (0, 1)


def marshal_curve(curve: Iterable[Point]) -> Mapping[str, str]:
    value = ";".join((f"{p.x:.{DECIMALS}f};{p.y:.{DECIMALS}f}" for p in curve))
    if len(value) > 0:
        value = f"{_SPLINE_CURVE_ID};{value};"
    else:
        value = f"{_LINEAR_CURVE_ID};"
    return {_TEMPLATE_FIELD: value}
