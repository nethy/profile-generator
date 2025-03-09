import math
from collections.abc import Callable, Iterable, Sequence
from functools import reduce
from typing import Optional

from profile_generator.main.profile_params import ColorGrades, Grading, Matte
from profile_generator.model import bezier, linalg
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Curve, Point, Vector

"""
Each tonal range has an anchor point which has it's defined color.
Between these points the colors are interpolated.

anchor points by default:

as+(am-as)/2 = 2(am-as)/2
as+(am-as)/2 = am-as
as = (am-as)/2
2as = am-as
as = am/3 = 0.5/3

shadows     16.667
midtones    50.000
highlights  83.333

balance:
    [0, 100], 0: midtones heavy, 50: equal, 100: shadows, highlights heavy
    ratio between shadows, highlights and midtones
    B = (1/4)^(1-b/100)*4^(b/100)
    shadow*((x-as)/(am-as))^B + midtone*(1-((x-as)/(am-as))^B)
origo:
    [0, 100]
    shifts tone ranges left and right
    P = 50 - p
    a+P
"""

_REF_COUNT = 20


def get_rgb_points(
    grading: Grading,
) -> Optional[tuple[Sequence[Point], Sequence[Point], Sequence[Point]]]:
    grade_lab = _get_color_grade_lab(grading.grades)
    grade_rgb = lambda lum: _lab_to_rgb(grade_lab(lum))
    matte_rgb = _get_matte_rgb(grading.matte)
    curve_rgb = lambda lum: linalg.map_vector(grade_rgb(lum), matte_rgb)
    ref_lums = (100 * i / (_REF_COUNT - 1) for i in range(_REF_COUNT))
    channels = [channel for channel in zip(*(curve_rgb(x) for x in ref_lums))]
    return (
        [Point(_srgb_luminance(x), value) for x, value in zip(ref_lums, channels[0])],
        [Point(_srgb_luminance(x), value) for x, value in zip(ref_lums, channels[1])],
        [Point(_srgb_luminance(x), value) for x, value in zip(ref_lums, channels[2])],
    )


def _get_color_grade_lab(color_grade: ColorGrades) -> Callable[[float], Vector]:
    pivot = color_grade.origo.value - 50
    balance = color_grade.balance.value / 100
    weight = math.pow((1 / 4), 1 - balance) * math.pow(4, balance)

    shadow_point = 100 / 6 + pivot
    midtone_point = 50.0 + pivot
    highlight_point = 100 * 5 / 6 + pivot

    global_lab = lab.from_lch(color_grade.global_lch.as_list())
    shadow_lab = lab.from_lch(color_grade.shadow_lch.as_list())
    midtone_lab = lab.from_lch(color_grade.midtone_lch.as_list())
    highlight_lab = lab.from_lch(color_grade.highlight_lch.as_list())
    shadow_lab = linalg.add_vectors(global_lab, shadow_lab)
    midtone_lab = linalg.add_vectors(global_lab, midtone_lab)
    highlight_lab = linalg.add_vectors(global_lab, highlight_lab)

    def _get_relative_lab(x: float) -> Vector:
        if x < shadow_point:
            return shadow_lab
        elif x < midtone_point:
            ratio = math.pow(
                (x - shadow_point) / (midtone_point - shadow_point), weight
            )
            return linalg.add_vectors(
                linalg.multiply_vector(shadow_lab, 1 - ratio),
                linalg.multiply_vector(midtone_lab, ratio),
            )
        elif x < highlight_point:
            ratio = math.pow(
                1 - (x - midtone_point) / (highlight_point - midtone_point), weight
            )
            return linalg.add_vectors(
                linalg.multiply_vector(midtone_lab, ratio),
                linalg.multiply_vector(highlight_lab, 1 - ratio),
            )
        else:
            return highlight_lab

    def _get_absolute_lab(x: float) -> Vector:
        lab = _get_relative_lab(x)
        lum = min(max(lab[0] + x, 0.0), 100.0)
        return [lum] + lab[1:]

    return _get_absolute_lab


def _get_matte_rgb(matte_param: Matte) -> Callable[[float], float]:
    shadow_offset = matte_param.shadow.value / 255
    highlight_offset = matte_param.highlight.value / 255
    shadow_boundary = 2 * shadow_offset
    highlight_boundary = 1 - 2 * (1 - highlight_offset)

    print(shadow_offset, shadow_boundary, highlight_offset, highlight_boundary)

    shadow_curve = _get_shadow_curve(shadow_offset, shadow_boundary)
    highlight_curve = _get_highlight_curve(highlight_offset, highlight_boundary)

    def _curve(x: float) -> float:
        if x < shadow_boundary:
            return shadow_curve(x)
        elif x < highlight_boundary:
            return x
        else:
            return highlight_curve(x)

    return _curve


def _get_shadow_curve(offset: float, boundary: float) -> Callable[[float], float]:
    if math.isclose(offset, 0):
        return lambda x: x

    a = offset / math.pow(boundary, 2)
    b = 1 - 2 * offset / boundary
    c = offset

    return lambda x: a * x * x + b * x + c


def _get_highlight_curve(offset: float, boundary: float) -> Callable[[float], float]:
    if math.isclose(offset, 1):
        return lambda x: x

    a = (offset - 1) / math.pow(boundary - 1, 2)
    b = (boundary - a * math.pow(boundary, 2) + a - offset) / (boundary - 1)
    c = offset - a - b

    return lambda x: a * x * x + b * x + c


def _lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def _srgb_luminance(lab_luminance: float) -> float:
    return SRGB.gamma(lab.to_xyz([lab_luminance, 0, 0])[1])
