from collections.abc import Mapping, Sequence
from typing import Any, Final, Optional

from profile_generator.model.color import rgb
from profile_generator.model.view import raw_therapee
from profile_generator.schema import SchemaField, object_of, range_of, type_of
from profile_generator.unit import Point

from .. import contrast_sigmoid


class Field:
    GREY18: Final = SchemaField("grey18", 90.0)
    SLOPE: Final = SchemaField("slope", 1.7)
    LINEAR_PROFILE: Final = SchemaField("linear_profile", True)


class Template:
    CURVE: Final = "Curve"
    CURVE2: Final = "Curve2"
    CAMERA_PROFILE_TONE_CURVE: Final = "CMToneCurve"
    CAMERA_PROFILE_LOOK_TABLE: Final = "CMApplyLookTable"


def _marshal_curve(curve: Optional[Sequence[Point]]) -> str:
    if curve is not None and len(curve) > 0:
        return raw_therapee.present_curve(raw_therapee.CurveType.STANDARD, curve)
    else:
        return raw_therapee.CurveType.LINEAR


def _process(data: Any) -> Mapping[str, str]:
    grey18 = rgb.normalize_value(data.get(*Field.GREY18))
    slope = data.get(*Field.SLOPE)
    linear_profile = data.get(*Field.LINEAR_PROFILE)
    flat = None
    if linear_profile:
        flat = contrast_sigmoid.flat(grey18)
    contrast = contrast_sigmoid.contrast(grey18, slope)
    return {
        Template.CURVE: _marshal_curve(flat),
        Template.CURVE2: _marshal_curve(contrast),
        Template.CAMERA_PROFILE_TONE_CURVE: str(not linear_profile).lower(),
        Template.CAMERA_PROFILE_LOOK_TABLE: str(not linear_profile).lower(),
    }


SCHEMA = object_of(
    {
        Field.GREY18.name: range_of(16.0, 240.0),
        Field.SLOPE.name: range_of(1.0, 5.0),
        Field.LINEAR_PROFILE.name: type_of(bool),
    },
    _process,
)
