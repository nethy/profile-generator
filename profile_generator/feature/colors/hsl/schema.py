from collections.abc import Iterable, Mapping
from typing import Any

from profile_generator.feature.colors.white_balance.schema import DEFAULT
from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of
from profile_generator.unit import Point

_LC_ENABLED = "LCEnabled"
_HH_CURVE = "HhCurve"
_CH_CURVE = "ChCurve"
_LH_CURVE = "LhCurve"

DEFAULT = {
    _HH_CURVE: raw_therapee.CurveType.LINEAR,
    _CH_CURVE: raw_therapee.CurveType.LINEAR,
    _LH_CURVE: raw_therapee.CurveType.LINEAR,
}

_STEPS = 7.0

_COLORS_SCHEMA = object_of(
    {
        "magenta": range_of(-_STEPS, _STEPS),
        "red": range_of(-_STEPS, _STEPS),
        "yellow": range_of(-_STEPS, _STEPS),
        "green": range_of(-_STEPS, _STEPS),
        "cyan": range_of(-_STEPS, _STEPS),
        "blue": range_of(-_STEPS, _STEPS),
    }
)

SCHEMA = object_of(
    {"hue": _COLORS_SCHEMA, "saturation": _COLORS_SCHEMA, "luminance": _COLORS_SCHEMA}
)

_BASE_VALUE = 0.5

_COLORS = [
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
]

HUES = {
    "red": 0 / 360,
    "yellow": 60 / 360,
    "green": 120 / 360,
    "cyan": 180 / 360,
    "blue": 240 / 360,
    "magenta": 300 / 360,
}


def process(data: Any) -> Mapping[str, str]:
    result: dict[str, str] = {}
    result |= _get_eq_curve(data, "hue", 0.25, _HH_CURVE)
    result |= _get_eq_curve(data, "saturation", 0.3, _CH_CURVE)
    result |= _get_eq_curve(data, "luminance", 0.07, _LH_CURVE)
    return DEFAULT | result


def _get_eq_curve(
    data: Any, key_name: str, max_adjustment: float, template_name: str
) -> Mapping[str, str]:
    config = data.get(key_name, {})
    equalizer = _get_equalizer(config, max_adjustment)
    if any(p.y != _BASE_VALUE for p in equalizer):
        return {
            _LC_ENABLED: "true",
            template_name: raw_therapee.CurveType.STANDARD
            + raw_therapee.present_linear_equalizer(equalizer),
        }
    else:
        return {}


def _get_equalizer(config: Mapping[str, int], max_adjustment: float) -> Iterable[Point]:
    return [
        Point(HUES[color], _get_value(config, color, max_adjustment))
        for color in _COLORS
    ]


def _get_value(config: Mapping[str, int], color: str, max_adjustment: float) -> float:
    adjustment = config.get(color, 0)
    return _BASE_VALUE + adjustment / _STEPS * max_adjustment
