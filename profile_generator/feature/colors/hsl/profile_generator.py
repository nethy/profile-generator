from collections.abc import Mapping, Sequence
from typing import Final

from profile_generator.main.profile_params import HueParams, ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint, LinearEqPoint


class Template:
    LC_ENABLED: Final = "LcEnabled"
    HH_CURVE: Final = "LcHhCurve"
    CH_CURVE: Final = "LcChCurve"
    LH_CURVE: Final = "LcLhCurve"

class HUE:
    RED: Final = 0 / 360
    YELLOW: Final = 60 / 360
    GREEN: Final = 120 / 360
    CYAN: Final = 180 / 360
    BLUE: Final = 240 / 360
    MAGENTA: Final = 300 / 360

DEFAULT = {
    Template.HH_CURVE: raw_therapee.CurveType.LINEAR,
    Template.CH_CURVE: raw_therapee.CurveType.LINEAR,
    Template.LH_CURVE: raw_therapee.CurveType.LINEAR,
}

def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    result: dict[str, str] = {}
    hsl = profile_params.colors.hsl
    result |= _get_eq_curve(hsl.hue, 0.25, Template.HH_CURVE)
    result |= _get_eq_curve(hsl.saturation, 0.3, Template.CH_CURVE)
    result |= _get_eq_curve(hsl.luminance, 0.07, Template.LH_CURVE)
    result[Template.LC_ENABLED] = str(len(result) > 0).lower()
    return DEFAULT | result

def _get_eq_curve(
        hue_params: HueParams, max_adjustment: float, template_name: str
) -> Mapping[str, str]:
    equalizer = _get_equalizer(hue_params, max_adjustment)
    if any(p.y != _BASE_VALUE for p in equalizer):
        return {
            template_name: raw_therapee.present_equalizer(equalizer),
        }
    else:
        return {}

def _get_equalizer(hue_params: HueParams, max_adjustment: float) -> Sequence[EqPoint]:
    return [
        LinearEqPoint(hue, _get_value(adjustment.value, max_adjustment))
        for hue, adjustment in (
            (HUE.RED, hue_params.red),
            (HUE.YELLOW, hue_params.yellow),
            (HUE.GREEN, hue_params.green),
            (HUE.CYAN, hue_params.cyan),
            (HUE.BLUE, hue_params.blue),
            (HUE.MAGENTA, hue_params.magenta),
        )
    ]

_BASE_VALUE = 0.5
_MAX = 10.0

def _get_value(adjustment: float, max_adjustment: float) -> float:
    return _BASE_VALUE + adjustment / _MAX * max_adjustment