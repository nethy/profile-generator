"""
Raw Therapee HSV equalizer functions

* hue: H = h + (f(h) - 0.5) * 2.0; h:[0,1]
    shifts hue value by +/-360 degree

    f(h) = (H - h) / 2.0 + 0.5

* sat: x = (f(h) - 0.5) * 2.0
    x: [-1, 1]
    x > 0:
        S = (1 - x) * s + x * (1 - (1 - s)^2)
        interpolate between the current and the *2 saturation
    x < 0:
        S = s * (1 + x)

    f(h) =
        S > s:
            S = s - sx + x * (1 - (1 - s)^2)
            S = s - x * (s + (1 - (1 - s)^2))
            s - S = x * (s + (1 - (1 - s)^2))
            x = (s - S) / (s + (1 - (1 - s)^2))
            (f(h) - 0.5) * 2.0 = (s - S) / (s + (1 - (1 - s)^2))
            f(h) = (s - S) / (s + (1 - (1 - s)^2)) / 2.0 + 0.5
        S < s:
            S = s * (1 + x)
            x = S / s - 1
            (f(h) - 0.5) * 2.0 = S / s - 1
            f(h) = (S / s - 1) / 2.0 + 0.5

* val: x = (f(h) - 0.5) * (1 - (1 - s)^4)
    x: [-0.5, 0.5]
    x > 0:
        V = (1 - x) * v + x * (1 - (1 - v)^2)
        interpolate between the current and the *1.5 value
    x < 0:
        V = v * (1 + x)

    f(h) =
        V > v:
            V = (1 - x) * v + x * (1 - (1 - v)^2)
            x = (v - V) / (v + (1 - (1 - v)^2))
            (f(h) - 0.5) * (1 - (1 - s)^4) = (v - V) / (v + (1 - (1 - v)^2))
            f(h)  = (v - V) / (v + (1 - (1 - v)^2)) / (1 - (1 - s)^4) + 0.5
        V < v:
            V = v * (1 + x)
            f(h) = (V / v - 1) / 2.0 + 0.5

"""

import math
from collections.abc import Mapping
from itertools import starmap
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint
from profile_generator.unit import Vector

from . import bsh


class Template:
    ENABLED: Final = "HSVEnabled"
    H_CURVE: Final = "HSVHCurve"
    S_CURVE: Final = "HSVSCurve"
    V_CURVE: Final = "HSVVCurve"


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    hsvs = bsh.get_hsvs(profile_params.colors.grading.bsh)
    hues = [EqPoint(x, y) for x, y in starmap(_get_hue, hsvs)]
    saturations = [EqPoint(x, y) for x, y in starmap(_get_saturation, hsvs)]
    values = [EqPoint(x, y) for x, y in starmap(_get_value, hsvs)]
    is_enabled = any(
        (not math.isclose(point.y, 0.5) for point in hues + saturations + values)
    )
    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.H_CURVE: raw_therapee.present_equalizer(hues),
        Template.S_CURVE: raw_therapee.present_equalizer(saturations),
        Template.V_CURVE: raw_therapee.present_equalizer(values),
    }


def _get_hue(ref_hsv: Vector, mod_hsv: Vector) -> tuple[float, float]:
    ref_h, mod_h = ref_hsv[0], mod_hsv[0]
    new_h = mod_h - ref_h
    return (ref_h, new_h / 2.0 + 0.5)


def _get_saturation(ref_hsv: Vector, mod_hsv: Vector) -> tuple[float, float]:
    ref_h, ref_s, mod_s = ref_hsv[0], ref_hsv[1], mod_hsv[1]
    if mod_s > ref_s:
        new_s = (ref_s - mod_s) / (ref_s + (1 - math.pow(1 - ref_s, 2)))
    else:
        new_s = mod_s / ref_s - 1
    return (ref_h, new_s / 2.0 + 0.5)


def _get_value(ref_hsv: Vector, mod_hsv: Vector) -> tuple[float, float]:
    ref_h, ref_s, ref_v, mod_v = ref_hsv[0], ref_hsv[1], ref_hsv[2], mod_hsv[2]
    if mod_v > ref_v:
        new_v = (
            (ref_v - mod_v)
            / (ref_v + (1 - math.pow(1 - ref_v, 2)))
            / (1 - math.pow(1 - ref_s, 4))
        ) + 0.5
    else:
        new_v = (mod_v / ref_v - 1) / 2.0 + 0.5
    return (ref_h, new_v)
