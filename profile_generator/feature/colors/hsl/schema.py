from collections.abc import Iterable, Mapping
from typing import Any, Final

from profile_generator.feature.colors.white_balance.schema import DEFAULT
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint, LinearEqPoint
from profile_generator.schema import object_of, range_of


class Field:
    HUE: Final = "hue"
    SATURATION: Final = "saturation"
    LUMINANCE: Final = "luminance"
    RED: Final = "red"
    YELLOW: Final = "yellow"
    GREEN: Final = "green"
    CYAN: Final = "cyan"
    BLUE: Final = "blue"
    MAGENTA: Final = "magenta"


class Template:
    LC_ENABLED: Final = "LCEnabled"
    HH_CURVE: Final = "HhCurve"
    CH_CURVE: Final = "ChCurve"
    LH_CURVE: Final = "LhCurve"


DEFAULT = {
    Template.LC_ENABLED: "false",
    Template.HH_CURVE: raw_therapee.CurveType.LINEAR,
    Template.CH_CURVE: raw_therapee.CurveType.LINEAR,
    Template.LH_CURVE: raw_therapee.CurveType.LINEAR,
}

_STEPS = 10.0

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
    {
        Field.HUE: _COLORS_SCHEMA,
        Field.SATURATION: _COLORS_SCHEMA,
        Field.LUMINANCE: _COLORS_SCHEMA,
    }
)

_BASE_VALUE = 0.5


HUES = {
    Field.RED: 0 / 360,
    Field.YELLOW: 60 / 360,
    Field.GREEN: 120 / 360,
    Field.CYAN: 180 / 360,
    Field.BLUE: 240 / 360,
    Field.MAGENTA: 300 / 360,
}


def process(data: Any) -> Mapping[str, str]:
    result: dict[str, str] = {}
    result |= _get_eq_curve(data, Field.HUE, 0.25, Template.HH_CURVE)
    result |= _get_eq_curve(data, Field.SATURATION, 0.3, Template.CH_CURVE)
    result |= _get_eq_curve(data, Field.LUMINANCE, 0.07, Template.LH_CURVE)
    return DEFAULT | result


def _get_eq_curve(
    data: Any, key_name: str, max_adjustment: float, template_name: str
) -> Mapping[str, str]:
    config = data.get(key_name, {})
    equalizer = _get_equalizer(config, max_adjustment)
    if any(p.y != _BASE_VALUE for p in equalizer):
        return {
            Template.LC_ENABLED: "true",
            template_name: raw_therapee.CurveType.STANDARD
            + raw_therapee.present_equalizer(equalizer),
        }
    else:
        return {}


def _get_equalizer(
    config: Mapping[str, int], max_adjustment: float
) -> Iterable[EqPoint]:
    return [
        LinearEqPoint(HUES[color], _get_value(config, color, max_adjustment))
        for color in (
            Field.RED,
            Field.YELLOW,
            Field.GREEN,
            Field.CYAN,
            Field.BLUE,
            Field.MAGENTA,
        )
    ]


def _get_value(config: Mapping[str, int], color: str, max_adjustment: float) -> float:
    adjustment = config.get(color, 0)
    return _BASE_VALUE + adjustment / _STEPS * max_adjustment
