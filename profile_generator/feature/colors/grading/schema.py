from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of, tuple_of

from . import grading


class Field:
    GLOBAL: Final = "global"
    SHADOW: Final = "shadow"
    MIDTONE: Final = "midtone"
    HIGHLIGHT: Final = "highlight"


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    R_CURVE: Final = "RGBCurvesRCurve"
    G_CURVE: Final = "RGBCurvesGCurve"
    B_CURVE: Final = "RGBCurvesBCurve"


_HCL_SCHEMA = tuple_of(range_of(0.0, 360.0), range_of(0.0, 10.0), range_of(-10.0, 10.0))

SCHEMA = object_of(
    {
        Field.GLOBAL: _HCL_SCHEMA,
        Field.SHADOW: _HCL_SCHEMA,
        Field.MIDTONE: _HCL_SCHEMA,
        Field.HIGHLIGHT: _HCL_SCHEMA,
    }
)

_DEFAULT_GRADE = [0.0, 0.0, 0.0]


def process(data: Any) -> Mapping[str, str]:
    global_hcl = data.get(Field.GLOBAL, _DEFAULT_GRADE)
    shadow_hcl = data.get(Field.SHADOW, _DEFAULT_GRADE)
    midtone_hcl = data.get(Field.MIDTONE, _DEFAULT_GRADE)
    highlight_hcl = data.get(Field.HIGHLIGHT, _DEFAULT_GRADE)
    rgb_curve_points = grading.rgb_curves(
        global_hcl, shadow_hcl, midtone_hcl, highlight_hcl
    )
    return {Template.ENABLED: "true"} | {
        template: raw_therapee.present_curve(raw_therapee.CurveType.STANDARD, points)
        for template, points in zip(
            [Template.R_CURVE, Template.G_CURVE, Template.B_CURVE], rgb_curve_points
        )
    }
