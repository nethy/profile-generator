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
"""

import math
from collections.abc import Callable, Mapping

from profile_generator.main.profile_params import LchAdjustment, ProfileParams
from profile_generator.model import hermite, interpolation
from profile_generator.model.color import lab
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Curve, curve

_SKIN_TONE_HUE_RANGE = (48.816, 89.129)


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    lch = profile_params.colors.grading.lch
    hue = get_adjustments(lch.hue, convert_to_hsv_hue)
    saturation = get_adjustments(lch.hue, convert_to_saturation)
    value = get_adjustments(lch.hue, convert_to_value)
    is_enabled = True
    return {
        "HSVEnabled": str(is_enabled).lower(),
        "HSVHCUrve": raw_therapee.present_linear_equalizer(curve.as_points(hue))
        if is_enabled
        else raw_therapee.CurveType.LINEAR,
        "HSVSCUrve": raw_therapee.present_linear_equalizer(curve.as_points(saturation))
        if is_enabled
        else raw_therapee.CurveType.LINEAR,
        "HSVVCUrve": raw_therapee.present_linear_equalizer(curve.as_points(value))
        if is_enabled
        else raw_therapee.CurveType.LINEAR,
    }


def get_adjustments(
    adjustment: LchAdjustment, convert_value: Callable[[float], float]
) -> Curve:
    adjustments = [
        (lab.to_rgb_hue(hue), convert_value(adjustment.value))
        for hue, adjustment in (
            (0, adjustment.magenta),
            (45, adjustment.orange),
            (90, adjustment.yellow),
            (135, adjustment.green),
            (180, adjustment.aqua),
            (225, adjustment.teal),
            (270, adjustment.blue),
            (315, adjustment.purple),
        )
        if not adjustment.is_set
    ]
    equalizer = _make_equalizer(adjustments)
    strength = adjustment.skin_tone_protection.value / 100
    return _clip(_apply_red_skin_protection(equalizer, _SKIN_TONE_HUE_RANGE, strength))


def convert_to_hsv_hue(value: float) -> float:
    difference = value * 3
    return difference / 2 + 0.5


def convert_to_saturation(value: float) -> float:
    scale = value / 10
    return (scale - 1) / 2 + 0.5


def convert_to_value(value: float) -> float:
    scale = 1 + value / 10 * 0.5
    return scale - 0.5


def convert_to_luminance(value: float) -> float:
    scale = 1 + value / 10 * 0.5
    if scale > 1:
        return (scale - 1) / 6 + 0.5
    else:
        return (scale - 1) / 1.9 + 0.5


def convert_to_chroma(value: float) -> float:
    scale = 1 + value / 10
    return (scale - 1) / 2 + 0.5


def convert_to_lch_hue(value: float) -> float:
    difference = value * 3
    return (difference / 180 * 3.14159) / 1.7 + 0.5


def _make_equalizer(adjustments: list[tuple[float, float]]) -> Curve:
    if len(adjustments) == 0:
        return lambda _: 0.5
    elif len(adjustments) == 1:
        return lambda _: adjustments[0][1]
    first, last = adjustments[0], adjustments[-1]
    adjustments.insert(0, (last[0] - 1.0, last[1]))
    adjustments.append((first[0] + 1.0, first[1]))
    return hermite.interpolate(adjustments)


def _apply_red_skin_protection(
    equalizer: Curve, hue_range: tuple[float, float], strength: float
) -> Curve:
    if math.isclose(strength, 0):
        return equalizer

    begin, end = lab.to_rgb_hue(hue_range[0]), lab.to_rgb_hue(hue_range[1])
    center = (begin + end) / 2

    def red_skin_protected(x: float) -> float:
        value = equalizer(x)
        if begin < x <= center:
            ratio = (x - begin) / (center - begin)
            value = interpolation.hermite(
                value, value * (1 - strength) + 0.5 * strength, ratio
            )
        elif center < x <= end:
            ratio = (x - center) / (end - center)
            value = interpolation.hermite(
                value * (1 - strength) + 0.5 * strength, value, ratio
            )

        return value

    return red_skin_protected


def _clip(fn: Curve) -> Curve:
    return lambda x: min(max(fn(x), 0), 1)
