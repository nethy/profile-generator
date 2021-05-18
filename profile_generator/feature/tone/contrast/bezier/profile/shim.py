from collections.abc import Iterable, Mapping
from typing import Any

from profile_generator.unit import DECIMALS, Point, Strength

_DEFAULT_GREY_X = 92
_DEFAULT_GREY_Y = 119
_DEFAULT_STRENGTH = 0
_DEFAULT_WEIGHTS = [1, 1]

_TEMPLATE_FIELD = "Curve"

_LINEAR_CURVE_ID = 0
_FLEXIBLE_CURVE_ID = 4


def get_arguments(
    configuration: Mapping[str, Any]
) -> tuple[Point, Strength, tuple[float, float]]:
    grey_point = _get_grey_point(configuration)
    strength = _get_strength(configuration)
    weights = _get_weights(configuration)
    return (grey_point, strength, weights)


def _get_grey_point(configuration: Mapping[str, Any]) -> Point:
    grey = configuration.get("grey", {})
    x = grey.get("x", _DEFAULT_GREY_X) / 255
    y = grey.get("y", _DEFAULT_GREY_Y) / 255
    return Point(x, y)


def _get_strength(configuration: Mapping[str, Any]) -> Strength:
    value = configuration.get("strength", _DEFAULT_STRENGTH)
    return Strength(value / 100)


def _get_weights(configuration: Mapping[str, Any]) -> tuple[float, float]:
    values = configuration.get("weights", _DEFAULT_WEIGHTS)
    return (values[0], values[1])


def marshal_curve(curve: Iterable[Point]) -> Mapping[str, str]:
    value = ";".join((f"{p.x:.{DECIMALS}f};{p.y:.{DECIMALS}f}" for p in curve))
    if len(value) > 0:
        value = f"{_FLEXIBLE_CURVE_ID};{value};"
    else:
        value = f"{_LINEAR_CURVE_ID};"
    return {_TEMPLATE_FIELD: value}
