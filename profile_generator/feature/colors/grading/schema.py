import math
from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model import linalg
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of, tuple_of
from profile_generator.unit import Point, Vector


class Field:
    SHADOW: Final = "shadow"
    MIDTONE: Final = "midtone"
    HIGHLIGHT: Final = "highlight"


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    R_CURVE: Final = "RGBCurvesRCurve"
    G_CURVE: Final = "RGBCurvesGCurve"
    B_CURVE: Final = "RGBCurvesBCurve"


_TINT_SCHEMA = tuple_of(
    range_of(-10.0, 10.0), range_of(0.0, 360.0), range_of(0.0, 10.0)
)

SCHEMA = object_of(
    {
        Field.SHADOW: _TINT_SCHEMA,
        Field.MIDTONE: _TINT_SCHEMA,
        Field.HIGHLIGHT: _TINT_SCHEMA,
    }
)

_DEFAULT_GRADE = [0.0, 0.0, 0.0]


def process(data: Any) -> Mapping[str, str]:
    shadow_grade = as_lab(*data.get(Field.SHADOW, _DEFAULT_GRADE))
    midtone_grade = as_lab(*data.get(Field.MIDTONE, _DEFAULT_GRADE))
    highlight_grade = as_lab(*data.get(Field.HIGHLIGHT, _DEFAULT_GRADE))
    if is_no_grading(shadow_grade, midtone_grade, highlight_grade):
        return {
            Template.ENABLED: "false",
            Template.R_CURVE: raw_therapee.CurveType.LINEAR,
            Template.G_CURVE: raw_therapee.CurveType.LINEAR,
            Template.B_CURVE: raw_therapee.CurveType.LINEAR,
        }
    rgb_curve_points = rgb_curves(shadow_grade, midtone_grade, highlight_grade)
    return {Template.ENABLED: "true"} | {
        template: raw_therapee.present_curve(raw_therapee.CurveType.STANDARD, points)
        for template, points in zip(
            [Template.R_CURVE, Template.G_CURVE, Template.B_CURVE], rgb_curve_points
        )
    }


def is_no_grading(
    shadow_grade: Vector, midtone_grade: Vector, highlight_grade: Vector
) -> bool:
    return math.isclose(
        sum(
            linalg.vector_length(grade)
            for grade in (shadow_grade, midtone_grade, highlight_grade)
        ),
        0,
    )


def as_lab(luminance: float, hue: float, chromaticity: float) -> Vector:
    radians = math.radians(hue)
    return [
        luminance,
        math.cos(radians) * chromaticity,
        math.sin(radians) * chromaticity,
    ]


def rgb_curves(
    shadow_grade: Vector, midtone_grade: Vector, highlight_grade: Vector
) -> list[list[Point]]:
    black = [0.0, 0.0, 0.0]
    shadow = [25.0 + shadow_grade[0]] + shadow_grade[1:]
    midtone = [50.0 + midtone_grade[0]] + midtone_grade[1:]
    highlight = [75.0 + highlight_grade[0]] + highlight_grade[1:]
    white = [100.0, 0.0, 0.0]
    tones = interpolate([black, shadow, midtone, highlight, white])
    rgbs = [lab_to_rgb(tone) for tone in tones]
    refs = [srgb_luminance(tone[0]) for tone in tones]
    return [
        [Point(*ref_rgb_value) for ref_rgb_value in zip(refs, rgb_values)]
        for rgb_values in zip(*rgbs)
    ]


def interpolate(items: list[Vector]) -> list[Vector]:
    result: list[list[float]] = []
    for i, item in enumerate(items):
        result.append(item)
        if i + 1 < len(items):
            interpolated = [(a + b) / 2 for a, b in zip(items[i], items[i + 1])]
            result.append(interpolated)
    return result


def lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def srgb_luminance(lab_luminance: float) -> float:
    return SRGB.gamma(lab.to_xyz([lab_luminance, 0, 0])[1])
