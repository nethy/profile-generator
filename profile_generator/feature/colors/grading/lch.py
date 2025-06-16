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

Skin tone:
    L: [59.7, 73.4]
    C: [13.2, 21.6]
    H: [54.0, 77.8]
"""

import math
from collections.abc import Callable, Sequence

from profile_generator.main.profile_params import LchAdjustment


def get_adjustments(
    adjustment: LchAdjustment, convert_value: Callable[[float], float]
) -> Sequence[tuple[float, float]]:
    return [
        (_lab_hue_to_rgb_hue(hue), convert_value(value))
        for hue, value in (
            (0, adjustment.magenta.value),
            (45, adjustment.orange.value),
            (90, adjustment.yellow.value),
            (135, adjustment.green.value),
            (180, adjustment.aqua.value),
            (225, adjustment.teal.value),
            (270, adjustment.blue.value),
            (315, adjustment.purple.value),
        )
    ]


def convert_luminance(value: float) -> float:
    target = 1 + value / 10 * 0.5
    if target > 1:
        return (target - 1) / 6 + 0.5
    else:
        return (target - 1) / 1.9 + 0.5


def convert_chroma(value: float) -> float:
    target = 1 + value / 10
    return (target - 1) / 2 + 0.5


def convert_hue(value: float) -> float:
    target = value * 3
    return (target / 180 * 3.14159) / 1.7 + 0.5



def _lab_hue_to_rgb_hue(lab_hue: float):
    lab_hue_in_radians = _to_radians(lab_hue)
    rgb_hue = 0.0

    if lab_hue_in_radians >= 0 and lab_hue_in_radians < 0.6:
        rgb_hue = 0.11666 * lab_hue_in_radians + 0.93
    elif lab_hue_in_radians >= 0.6 and lab_hue_in_radians < 1.4:
        rgb_hue = 0.1125 * lab_hue_in_radians - 0.0675
    elif lab_hue_in_radians >= 1.4 and lab_hue_in_radians < 2:
        rgb_hue = 0.2666 * lab_hue_in_radians - 0.2833
    elif lab_hue_in_radians >= 2 and lab_hue_in_radians < 3.14159:
        rgb_hue = 0.1489 * lab_hue_in_radians - 0.04785
    elif lab_hue_in_radians >= -3.14159 and lab_hue_in_radians < -2.8:
        rgb_hue = 0.23419 * lab_hue_in_radians + 1.1557
    elif lab_hue_in_radians >= -2.8 and lab_hue_in_radians < -2.3:
        rgb_hue = 0.16 * lab_hue_in_radians + 0.948
    elif lab_hue_in_radians >= -2.3 and lab_hue_in_radians < -0.9:
        rgb_hue = 0.12143 * lab_hue_in_radians + 0.85928
    elif lab_hue_in_radians >= -0.9 and lab_hue_in_radians < -0.1:
        rgb_hue = 0.2125 * lab_hue_in_radians + 0.94125
    elif lab_hue_in_radians >= -0.1 and lab_hue_in_radians < 0:
        rgb_hue = 0.1 * lab_hue_in_radians + 0.93

    if rgb_hue < 0.0:
        rgb_hue += 1.0
    elif rgb_hue > 1.0:
        rgb_hue -= 1.0

    return rgb_hue


def _to_radians(degree: float):
    """
    0..360 -> -pi..pi
    """
    return round(math.radians(degree if degree < 180 else degree - 360), 5)
