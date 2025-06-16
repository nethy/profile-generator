import bisect
from collections.abc import Callable
from operator import itemgetter
from typing import TypeAlias

from profile_generator.main.profile_params import ColorToning, ColorToningChannel
from profile_generator.model import interpolation
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Vector

ColorTone: TypeAlias = tuple[float, Vector]


def get_rgb_toning(
    color_toning: ColorToning,
) -> Callable[[float], Vector]:
    lab_mapping = get_lab_toning(color_toning)
    return _as_rgb(lab_mapping)


def _as_rgb(lab_toning: Callable[[float], Vector]) -> Callable[[float], Vector]:
    def rgb_toning(rgb: float) -> Vector:
        luminance = lab.from_xyz(xyz.from_rgb([rgb] * 3, SRGB))[0]
        lab_color = lab_toning(luminance)
        return xyz.to_rgb(lab.to_xyz(lab_color), SRGB)

    return rgb_toning


def get_lab_toning(color_toning: ColorToning) -> Callable[[float], Vector]:
    tones = _get_tones(color_toning)

    def lab_curve(x: float) -> Vector:
        i = bisect.bisect(tones, x, key=itemgetter(0))
        if i == 0:
            return tones[0][1]
        elif i == len(tones):
            return tones[-1][1]
        else:
            return _interpolate(x, tones[i - 1], tones[i])

    if len(tones) > 0:
        return lab_curve
    else:
        return lambda x: [x, 0, 0]


def _get_tones(color_toning: ColorToning) -> list[ColorTone]:
    channel = color_toning.channels.value
    if channel == ColorToningChannel.ONE:
        return [
            _to_lab(0.0, [0, 0, 0]),
            _to_lab(50.0, color_toning.midtone.as_list()),
            _to_lab(100.0, [0, 0, 0]),
        ]
    elif channel == ColorToningChannel.TWO:
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
    return (luminance, lab.from_lch([_clip(luminance + l, 0, 100), c, h]))


def _clip(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)


def _interpolate(x: float, left: ColorTone, right: ColorTone) -> Vector:
    return [
        interpolation.interpolate_values(
            left[1][0], right[1][0], interpolation.linear, x, left[0], right[0]
        ),
        interpolation.interpolate_values(
            left[1][1], right[1][1], interpolation.hermite, x, left[0], right[0]
        ),
        interpolation.interpolate_values(
            left[1][2], right[1][2], interpolation.hermite, x, left[0], right[0]
        ),
    ]
