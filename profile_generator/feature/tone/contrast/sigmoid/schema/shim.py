from collections.abc import Mapping, Sequence
from typing import Any, Final

from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_GREY18 = 90.0
_DEFAULT_SLOPE = 1.0


class Template:
    CURVE: Final = "Curve"
    CURVE2: Final = "Curve2"


def get_parameters(configuration: Mapping[str, Any]) -> tuple[float, ...]:
    grey18 = configuration.get("grey18", _DEFAULT_GREY18)
    slope = configuration.get("slope", _DEFAULT_SLOPE)
    return (grey18, slope)


def marshal(flat: Sequence[Point], contrast: Sequence[Point]) -> Mapping[str, str]:
    return {
        Template.CURVE: _marshal_curve(flat),
        Template.CURVE2: _marshal_curve(contrast),
    }


def _marshal_curve(curve: Sequence[Point]) -> str:
    if len(curve) > 0:
        return raw_therapee.present_curve(raw_therapee.CurveType.STANDARD, curve)
    else:
        return raw_therapee.CurveType.LINEAR
