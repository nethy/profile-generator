import bisect
import math
from collections.abc import Callable, Sequence
from operator import itemgetter
from typing import TypeAlias

from profile_generator.main.profile_params import ColorToning, ColorToningChannel
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space.srgb import SRGB
from profile_generator.unit import Vector
from profile_generator.unit.point import Point

ColorTone: TypeAlias = tuple[float, Vector]


def get_rgb_points(
    color_toning: ColorToning,
) -> tuple[Sequence[Point], Sequence[Point], Sequence[Point]]:
    lab_mapping = get_lab_mapping(color_toning)
    rgb_points = _get_rgb_points(lab_mapping)
    red, green, blue = [], [], []
    for x, r, g, b in rgb_points:
        red.append(Point(x, _clip(r, 0, 1)))
        green.append(Point(x, _clip(g, 0, 1)))
        blue.append(Point(x, _clip(b, 0, 1)))
    return (red, green, blue)


_POINT_COUNT = 32


def _get_rgb_points(color_mapping: Callable[[float], Vector]) -> Sequence[Vector]:
    return [
        [x]
        + xyz.to_rgb(
            lab.to_xyz(color_mapping(lab.from_xyz(xyz.from_rgb([x] * 3, SRGB))[0])),
            SRGB,
        )
        for x in (i / _POINT_COUNT for i in range(_POINT_COUNT + 1))
    ]


def get_lab_mapping(color_toning: ColorToning) -> Callable[[float], Vector]:
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
    ratio = (x - left[0]) / (right[0] - left[0])
    luma_weight = _linear_weight(ratio)
    # chroma_weight = _linear_weight(ratio)
    chroma_weight = _non_linear_weight(ratio)
    return [
        luma_weight * left[1][0] + (1 - luma_weight) * right[1][0],
        chroma_weight * left[1][1] + (1 - chroma_weight) * right[1][1],
        chroma_weight * left[1][2] + (1 - chroma_weight) * right[1][2],
    ]


def _linear_weight(x: float) -> float:
    return 1 - x


def _non_linear_weight(x: float) -> float:
    return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1
