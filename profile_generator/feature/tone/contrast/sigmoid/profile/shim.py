from typing import Any, Tuple

from profile_generator.unit import Point, Strength

_DEFAULT_GREY_X = 92
_DEFAULT_GREY_Y = 119
_DEFAULT_STRENGTH = 0

_TEMPLATE_FIELD = "Curve"

_LINEAR_CURVE_ID = 0
_SPLINE_CURVE_ID = 1
_FLEXIBLE_CURVE_ID = 4


def get_parameters(configuration: dict[str, Any]) -> Tuple[Point, Strength]:
    grey = _get_grey(configuration)
    strength = _get_strength(configuration)
    return (
        grey,
        strength,
    )


def _get_grey(configuration: dict[str, Any]) -> Point:
    grey = configuration.get("grey", {})
    x = grey.get("x", _DEFAULT_GREY_X) / 255
    y = grey.get("y", _DEFAULT_GREY_Y) / 255
    return Point(x, y)


def _get_strength(configuration: dict[str, Any]) -> Strength:
    value = configuration.get("strength", _DEFAULT_STRENGTH) / 100
    return Strength(value)


def marshal_curve(curve: list[Point]) -> dict[str, str]:
    value = ";".join((f"{p.x:.5f};{p.y:.5f}" for p in curve))
    if len(value) > 0:
        value = f"{_SPLINE_CURVE_ID};{value};"
    else:
        value = f"{_LINEAR_CURVE_ID};"
    return {_TEMPLATE_FIELD: value}
