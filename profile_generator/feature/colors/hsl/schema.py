from collections.abc import Mapping
from typing import Any

from profile_generator.feature.colors.white_balance.schema import DEFAULT
from profile_generator.model.color import rgb
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of
from profile_generator.unit import Point

_STEPS = 5

_LAB_ENABLED = "LabEnabled"
_HH_CURVE = "HhCurve"
_CH_CURVE = "ChCurve"
_LH_CURVE = "LhCurve"

DEFAULT = {
    _HH_CURVE: raw_therapee.CurveType.LINEAR,
    _CH_CURVE: raw_therapee.CurveType.LINEAR,
    _LH_CURVE: raw_therapee.CurveType.LINEAR,
}

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


class HUE:
    BLUE = rgb.rgb_to_hsv(ColorChart.BLUE)[0]
    GREEN = rgb.rgb_to_hsv(ColorChart.GREEN)[0]
    RED = rgb.rgb_to_hsv(ColorChart.RED)[0]
    YELLOW = rgb.rgb_to_hsv(ColorChart.YELLOW)[0]
    MAGENTA = rgb.rgb_to_hsv(ColorChart.MAGENTA)[0]
    CYAN = rgb.rgb_to_hsv(ColorChart.CYAN)[0]


_BASE_VALUE = 0.5


def process(data: Any) -> Mapping[str, str]:
    result: dict[str, str] = {}
    result |= _get_eq_curve(data, "hue", 0.5, _HH_CURVE)
    result |= _get_eq_curve(data, "saturation", 0.3, _CH_CURVE)
    result |= _get_eq_curve(data, "luminance", 0.3, _LH_CURVE)
    if len(result) > 0:
        result[_LAB_ENABLED] = "true"
    return DEFAULT | result


def _get_eq_curve(
    data: Any, key_name: str, max_adjustment: float, template_name: str
) -> Mapping[str, str]:
    config = data.get(key_name, {})
    equalizer = _get_equalizer(config, max_adjustment)
    if len(equalizer) > 0:
        return {
            template_name: raw_therapee.CurveType.STANDARD
            + raw_therapee.present_equalizer(equalizer)
        }
    else:
        return {}


def _get_equalizer(config: Mapping[str, int], max_adjustment: float) -> list[Point]:
    return sorted(
        [
            Point(_hue_of(color), _adjustment_of(adjustment, max_adjustment))
            for color, adjustment in config.items()
        ]
    )


def _hue_of(color: str) -> float:
    return getattr(HUE, color.upper())


def _adjustment_of(adjustment: int, maximum: float) -> float:
    return _BASE_VALUE + adjustment / _STEPS * maximum
