import bisect
import math
import operator
from collections.abc import Callable
from typing import TypeAlias

from profile_generator.main.profile_params import ColorToning, ColorToningChannel
from profile_generator.model.color import lab
from profile_generator.unit import Vector

ColorTone: TypeAlias = tuple[float, Vector]


def get_lab_mapping(params: ColorToning) -> Callable[[float], Vector]:
    tones = _get_tones(params)

    def lab_curve(x: float) -> Vector:
        i = bisect.bisect(tones, x, key=lambda item: item[0])
        if i == 0:
            lab = tones[0][1]
        elif i == len(tones):
            lab = tones[-1][1]
        else:
            lab = _interpolate(x, tones[i-1], tones[i])
        return [a + b for a, b in zip(lab, [x, 0, 0])]

    if len(tones) > 0:
        return lab_curve
    else:
        return lambda x: [x, 0, 0]


def _get_tones(color_toning: ColorToning) -> list[ColorTone]:
    channel = color_toning.channels.value
    if channel == ColorToningChannel.TWO:
        return [
            _to_lab(0.0, color_toning.black.as_list()),
            _to_lab(100 * 1 / 3, color_toning.shadow.as_list()),
            _to_lab(100 * 2 / 3, color_toning.highlight.as_list()),
            _to_lab(100.0, color_toning.white.as_list()),
        ]
    elif channel == ColorToningChannel.THREE:
        return [
            _to_lab(0.0, color_toning.black.as_list()),
            _to_lab(25.0, color_toning.shadow.as_list()),
            _to_lab(50.0, color_toning.midtone.as_list()),
            _to_lab(75.0, color_toning.highlight.as_list()),
            _to_lab(100.0, color_toning.white.as_list()),
        ]
    else:
        raise ValueError(f"Unhandled value: {channel}")


def _to_lab(luminance: float, lch_tone: Vector) -> ColorTone:
    l, c, h = lch_tone
    return (luminance, lab.from_lch([luminance + l, c, h]))



def _interpolate(x: float, left: ColorTone, right: ColorTone) -> Vector:
    weight = _weight((x - left[0]) / (right[0] - left[0]))
    return [
        weight * a + (1 - weight) * b
        for a, b in zip(left[1], right[1])
    ]

def _weight(x: float) -> float:
    return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1
