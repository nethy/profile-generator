from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

from .highlight import Highlight

_DEFAULT_GREY18 = 90.0
_DEFAULT_SLOPE = 1.0
_DEFAULT_EV_COMP = 0.0
_DEFAULT_HIGHLIGHT = Highlight.SOFT

_CURVE = "Curve"


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[float, float, float, Highlight]:
    grey18 = configuration.get("grey18", _DEFAULT_GREY18)
    slope = configuration.get("slope", _DEFAULT_SLOPE)
    brightness = configuration.get("brightness", _DEFAULT_EV_COMP)
    highlight = _get_highlight(configuration)
    return (grey18, slope, brightness, highlight)


def _get_highlight(configuration: Mapping[str, Any]) -> Highlight:
    value = configuration.get("highlight", _DEFAULT_HIGHLIGHT.name)
    return Highlight[value.upper()]


def marshal_curve(curve: Sequence[Point]) -> Mapping[str, str]:
    value = raw_therapee.CurveType.LINEAR
    if len(curve) > 0:
        value = raw_therapee.CurveType.STANDARD + raw_therapee.present_curve(curve)
    return {_CURVE: value}
