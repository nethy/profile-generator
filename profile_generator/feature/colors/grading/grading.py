import math
from collections.abc import Iterable

from profile_generator.model import linalg
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Point, Vector


def rgb_curves(
    global_hcl: Vector, shadow_hcl: Vector, midtone_hcl: Vector, highlight_hcl: Vector
) -> list[list[Point]]:
    grades = _get_grades(global_hcl, shadow_hcl, midtone_hcl, highlight_hcl)
    tones = _get_tones(*grades)
    tones = _interpolate(tones)
    rgbs = [_lab_to_rgb(tone) for tone in tones]
    refs = [_srgb_luminance(tone[0]) for tone in tones]
    return [
        [Point(ref, value) for ref, value in zip(refs, channel)]
        for channel in zip(*rgbs)
    ]


def _get_grades(
    global_hcl: Vector, shadow_hcl: Vector, midtone_hcl: Vector, highlight_hcl: Vector
) -> Iterable[Vector]:
    global_grade, shadow_grade, midtone_grade, highlight_grade = map(
        _as_lab, (global_hcl, shadow_hcl, midtone_hcl, highlight_hcl)
    )
    return map(
        lambda grade: linalg.add_vector(grade, global_grade),
        (shadow_grade, midtone_grade, highlight_grade),
    )


def _as_lab(hcl: Vector) -> Vector:
    hue, chromaticity, luminance = hcl
    radians = math.radians(hue)
    return [
        luminance,
        math.cos(radians) * chromaticity,
        math.sin(radians) * chromaticity,
    ]


def _get_tones(
    shadow_grade: Vector, midtone_grade: Vector, highlight_grade: Vector
) -> list[Vector]:
    black = [0.0, 0.0, 0.0]
    shadow = [25.0 + shadow_grade[0]] + shadow_grade[1:]
    midtone = [50.0 + midtone_grade[0]] + midtone_grade[1:]
    highlight = [75.0 + highlight_grade[0]] + highlight_grade[1:]
    white = [100.0, 0.0, 0.0]
    return [black, shadow, midtone, highlight, white]


def _interpolate(items: list[Vector]) -> list[Vector]:
    result: list[list[float]] = []
    for i, item in enumerate(items):
        result.append(item)
        if i + 1 < len(items):
            interpolated = [(a + b) / 2 for a, b in zip(items[i], items[i + 1])]
            result.append(interpolated)
    return result


def _lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def _srgb_luminance(lab_luminance: float) -> float:
    return SRGB.gamma(lab.to_xyz([lab_luminance, 0, 0])[1])
