from collections.abc import Mapping
from typing import Any, Final

from profile_generator import Hcl, ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.schema import object_of, range_of, tuple_of
from profile_generator.unit import Vector

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
    if len(rgb_curve_points) > 0:
        return {Template.ENABLED: "true"} | {
            template: raw_therapee.present_curve(
                raw_therapee.CurveType.STANDARD, points
            )
            for template, points in zip(
                [Template.R_CURVE, Template.G_CURVE, Template.B_CURVE], rgb_curve_points
            )
        }
    else:
        return {
            Template.ENABLED: "false",
            Template.R_CURVE: raw_therapee.CurveType.LINEAR,
            Template.G_CURVE: raw_therapee.CurveType.LINEAR,
            Template.B_CURVE: raw_therapee.CurveType.LINEAR,
        }


def _parse(data: Any, profile_params: ProfileParams) -> None:
    _hcl_parse(profile_params.color.grading.base, data.get(Field.GLOBAL))
    _hcl_parse(profile_params.color.grading.shadow, data.get(Field.SHADOW))
    _hcl_parse(profile_params.color.grading.midtone, data.get(Field.MIDTONE))
    _hcl_parse(profile_params.color.grading.highlight, data.get(Field.HIGHLIGHT))


def _hcl_parse(hcl: Hcl, data: Vector) -> None:
    hcl.hue, hcl.chromacity, hcl.luminance = data
