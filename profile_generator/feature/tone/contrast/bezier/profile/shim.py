from typing import Any, Collection, Dict, Tuple

from unit import Point, Strength

_DEFAULT_GREY = [92, 119]
_DEFAULT_STRENGTH = 0

_TEMPLATE_FIELD = "Curve"

_LINEAR_CURVE_ID = 0
_STD_CURVE_ID = 1


def get_arguments(configuration: Dict[str, Any]) -> Tuple[Point, Strength]:
    grey_point = _get_grey_point(configuration)
    strength = _get_strength(configuration)
    return (grey_point, strength)


def _get_grey_point(configuration: Dict[str, Any]) -> Point:
    grey_configuration = configuration.get("middle_grey", _DEFAULT_GREY)
    x = grey_configuration[0] / 255
    y = grey_configuration[1] / 255
    return Point(x, y)


def _get_strength(configuration: Dict[str, Any]) -> Strength:
    value = configuration.get("strength", _DEFAULT_STRENGTH)
    return Strength(value / 100)


def marshal_curve(curve: Collection[Point]) -> Dict[str, str]:
    value = ";".join((f"{p.x:.5f};{p.y:.5f}" for p in curve))
    if len(value) > 0:
        value = f"{_STD_CURVE_ID};{value};"
    else:
        value = f"{_LINEAR_CURVE_ID};"
    return {_TEMPLATE_FIELD: value}
