"""
RawTherapee LCH Curves:

lab_hue in -pi..pi
rgb_hue in   0..1

On the UI the hue is in rgb hue.

CH curve:
    C = (1 + (f(h) - 0.5) * 2) * c
    f(h) = (C/c-1)/2+0.5

HH curve:
    H =(f(h)-0.5)*1.7+h
    f(h) = (H-h)/1.7+0.5

LH curve:
    f(h) > 0.5
        x = (f(h) - 0.5) * 2
        L = (1-x)*l+x*(1-(1-l)^4)
        L' = 1-x+x*4*(1-l)^3
        x = (L'(0)-1)/3

        2*f(h)-1 = (L'-1)/3
        f(h) = (L'-1)/6+0.5
    f(h) <= 0.5
        x = (f(h) - 0.5) * 1.9
        L = l * (1+x)
        x = L/l-1
        f(h) = (L/l-1)/1.9+0.5

Hue Curve
    H = (f(h)-0.5)*2+h
    f(h) = (H-h)/2+0.5

Saturation Curve
    f(h) > 0.5:
        S' = (1-(f(h)-0.5)*2)-2*(f(h)-0.5)*2*(1-s)*(-1), s=0
        S' = 1+2*(f(h)-0.5)
        f(h) = (S'-1)/2+0.5
    f(h) < 0.5:
        S = s*(1+2*(f(h)-0.5))
        f(h) = (S/s-1)/2+0.5

Value Curve
    f(h) > 0.5:
        V' = (1-f(h)-0.5)-2*(f(h)-0.5)*(1-v)*(-1), v=0
        V' = 1+f(h)-0.5
        f(h) = V'-0.5
    f(h) < 0.5:
        V = v * (1+f(h)-0.5)
        V = v*(0.5+f(h))
        f(h) = V/v-0.5

Skin tonal range reference:
https://skintone.google/

skin tone range [45, 85]
"""

import bisect
from collections.abc import Callable, Mapping
from typing import Sequence

from profile_generator.main.profile_params import LchAdjustment, ProfileParams
from profile_generator.model.color import lab
from profile_generator.model.color_chart import ColorChartLab
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Vector
from profile_generator.unit.line import Line
from profile_generator.unit.point import Point

_SKIN_TONE_HUE_RANGE = (45, 85)


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    hsv = profile_params.colors.grading.hsv
    hue = get_adjustments(hsv.hue, _convert_to_hsv_hue)
    saturation = get_adjustments(hsv.saturation, _convert_to_saturation)
    value = get_adjustments(hsv.value, _convert_to_value)
    is_enabled = any(len(eq) > 0 for eq in (hue, saturation, value))
    return {
        "HSVEnabled": str(is_enabled).lower(),
        "HSVHCurve": (raw_therapee.present_linear_equalizer(hue)),
        "HSVSCurve": (raw_therapee.present_linear_equalizer(saturation)),
        "HSVVCurve": (raw_therapee.present_linear_equalizer(value)),
    }


def get_adjustments(
    adjustment: LchAdjustment, convert: Callable[[float], float]
) -> Sequence[Point]:
    adjustments = [
        (hue, convert(adjustment.value))
        for hue, adjustment in (
            (_get_hue(ColorChartLab.RED), adjustment.red),
            (_get_hue(ColorChartLab.YELLOW), adjustment.yellow),
            (_get_hue(ColorChartLab.GREEN), adjustment.green),
            (_get_hue(ColorChartLab.CYAN), adjustment.cyan),
            (_get_hue(ColorChartLab.BLUE), adjustment.blue),
            (_get_hue(ColorChartLab.MAGENTA), adjustment.magenta),
        )
        if adjustment.is_set
    ]
    skin_tone_protection = adjustment.skin_tone_protection.value / 100
    equalizer = _make_lch_equalizer(adjustments, skin_tone_protection)
    return sorted([Point(lab.to_rgb_hue(x), y) for x, y in equalizer])


def _get_hue(color: Vector) -> float:
    return lab.to_lch(color)[2]


def _convert_to_hsv_hue(value: float) -> float:
    difference = value * 3 / 360
    return difference / 2 + 0.5


def _convert_to_saturation(value: float) -> float:
    scale = value / 10
    return (scale - 1) / 2 + 0.5


def _convert_to_value(value: float) -> float:
    scale = 1 + value / 10 * 0.5
    return scale - 0.5


def _convert_to_luminance(value: float) -> float:
    scale = 1 + value / 10 * 0.5
    if scale > 1:
        return (scale - 1) / 6 + 0.5
    else:
        return (scale - 1) / 1.9 + 0.5


def _convert_to_chroma(value: float) -> float:
    scale = 1 + value / 10
    return (scale - 1) / 2 + 0.5


def _convert_to_lch_hue(value: float) -> float:
    difference = value * 3
    return (difference / 180 * 3.14159) / 1.7 + 0.5


def _make_lch_equalizer(
    adjustments: list[tuple[float, float]], skin_tone_protection: float
) -> list[Point]:
    equalizer = [Point(x, y) for x, y in adjustments]

    if len(equalizer) == 0:
        return equalizer

    if skin_tone_protection > 0.1:
        skin_tone_begin, skin_tone_end = _SKIN_TONE_HUE_RANGE
        skin_tone_center = (skin_tone_begin + skin_tone_end) / 2
        _add_eq_point(equalizer, skin_tone_begin, 0.0)
        _add_eq_point(equalizer, skin_tone_center, skin_tone_protection)
        _add_eq_point(equalizer, skin_tone_end, 0.0)

    return equalizer


def _add_eq_point(equalizer: list[Point], x: float, protection: float) -> None:
    length = len(equalizer)
    i = bisect.bisect(equalizer, x, key=lambda point: point.x)
    line = Line.from_points(equalizer[(i - 1) % length], equalizer[i % length])
    equalizer.insert(i, Point(x, (1 - protection) * line.get_y(x) + protection * 0.5))
