from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.color import constants, rgb
from profile_generator.model.view import raw_therapee
from profile_generator.schema import SchemaField, object_of, range_of, type_of

from .. import contrast_sigmoid


class Field:
    GREY18: Final = SchemaField("grey18", 90.0)
    SLOPE: Final = SchemaField("slope", 1.6)
    LINEAR_PROFILE: Final = SchemaField("linear_profile", True)


class Template:
    CURVE: Final = "Curve"
    L_CURVE: Final = "LCurve"
    AB_CURVE: Final = "ABCurve"
    CAMERA_PROFILE_TONE_CURVE: Final = "CMToneCurve"
    CAMERA_PROFILE_LOOK_TABLE: Final = "CMApplyLookTable"


def _process(data: Any) -> Mapping[str, str]:
    grey18 = rgb.normalize_value(data.get(*Field.GREY18))
    slope = data.get(*Field.SLOPE)
    linear_profile = data.get(*Field.LINEAR_PROFILE)
    corrected_slope = contrast_sigmoid.compensate_slope(grey18, slope)
    if linear_profile:
        luminance_curve = contrast_sigmoid.get_tone_curve(grey18, corrected_slope)
    else:
        luminance_curve = contrast_sigmoid.get_contrast(corrected_slope)
    chromaticity_curve = contrast_sigmoid.get_chromaticity_curve(corrected_slope)
    return {
        Template.CURVE: _get_correction_params(grey18, linear_profile),
        Template.L_CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, luminance_curve
        ),
        Template.AB_CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, chromaticity_curve
        ),
        Template.CAMERA_PROFILE_TONE_CURVE: str(not linear_profile).lower(),
        Template.CAMERA_PROFILE_LOOK_TABLE: str(not linear_profile).lower(),
    }


def _get_correction_params(grey18: float, linear_profile: bool) -> str:
    midtone = constants.GREY18_SRGB
    if linear_profile:
        midtone = grey18

    return (
        "2;"
        + ";".join(
            (
                str(round(i, 9))
                for i in ([midtone / 2, midtone, (midtone + 1) / 2] + [0] * 4)
            )
        )
        + ";"
    )


SCHEMA = object_of(
    {
        Field.GREY18.name: range_of(16.0, 240.0),
        Field.SLOPE.name: range_of(1.0, 5.0),
        Field.LINEAR_PROFILE.name: type_of(bool),
    },
    _process,
)
