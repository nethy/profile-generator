from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee

from . import grading


class Template:
    ENABLED: Final = "RGBCurvesEnabled"
    R_CURVE: Final = "RGBCurvesRCurve"
    G_CURVE: Final = "RGBCurvesGCurve"
    B_CURVE: Final = "RGBCurvesBCurve"


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    global_hcl = profile_params.colors.grading.base.as_list()
    shadow_hcl = profile_params.colors.grading.shadow.as_list()
    midtone_hcl = profile_params.colors.grading.midtone.as_list()
    highlight_hcl = profile_params.colors.grading.highlight.as_list()
    rgb_curve_points = grading.get_rgb_curves(
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
