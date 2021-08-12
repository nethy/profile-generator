from collections.abc import Mapping, Sequence
from typing import Any

from profile_generator.model.linalg import Vector
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_DEFAULT_NETRUAL5: Vector = [90, 90, 90]
_DEFAULT_EV_COMP = 0.0
_DEFAULT_GAMMA = 1.0

_CURVE = "Curve"
_CURVE2 = "Curve2"


def get_parameters(
    configuration: Mapping[str, Any]
) -> tuple[Vector, float, float, tuple[float, float]]:
    netrual5 = configuration.get("neutral5", _DEFAULT_NETRUAL5)
    ev_comp = configuration.get("exposure_compensation", _DEFAULT_EV_COMP)
    gamma = configuration.get("gamma", _DEFAULT_GAMMA)
    offsets = _get_offsets(configuration)
    return (netrual5, gamma, ev_comp, offsets)


def _get_offsets(configuration: Mapping[str, Any]) -> tuple[float, float]:
    matte_effect = configuration.get("matte_effect", False)
    if matte_effect:
        return (16 / 255, 1.0)
    else:
        return (0, 1)


def marshal_curves(
    control_curve: Sequence[Point], contrast_curve: Sequence[Point]
) -> Mapping[str, str]:
    control_curve_value = raw_therapee.CurveType.LINEAR
    if len(control_curve) > 0:
        control_curve_value = (
            raw_therapee.CurveType.CONTROL_CAGE
            + raw_therapee.present_curve(control_curve)
        )
    value = raw_therapee.CurveType.LINEAR
    if len(contrast_curve) > 0:
        value = raw_therapee.CurveType.STANDARD + raw_therapee.present_curve(
            contrast_curve
        )
    return {_CURVE: control_curve_value, _CURVE2: value}
